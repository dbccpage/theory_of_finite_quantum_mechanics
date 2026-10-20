//! Exact JSON admission: inexact number tokens and duplicate object keys are refused
//! on the raw text, before `serde_json` keeps the last duplicate and drops the earlier one.

pub fn admit_exact_json(input: &str) -> Result<(), String> {
    let mut scan = Scan {
        text: input,
        i: 0,
        deferred: None,
    };
    scan.skip_ws();
    if scan.eof() {
        return Ok(());
    }
    scan.value()?;
    scan.skip_ws();
    if !scan.eof() {
        return Err("INVALID_JSON:trailing input".into());
    }
    scan.deferred.map_or(Ok(()), Err)
}

struct Scan<'a> {
    text: &'a str,
    i: usize,
    deferred: Option<String>,
}

impl<'a> Scan<'a> {
    fn eof(&self) -> bool {
        self.i >= self.text.len()
    }

    fn peek(&self) -> Option<char> {
        self.text[self.i..].chars().next()
    }

    fn bump(&mut self) -> Option<char> {
        let c = self.peek()?;
        self.i += c.len_utf8();
        Some(c)
    }

    fn skip_ws(&mut self) {
        while matches!(self.peek(), Some(' ' | '\n' | '\r' | '\t')) {
            self.bump();
        }
    }

    fn value(&mut self) -> Result<(), String> {
        self.skip_ws();
        match self.peek() {
            Some('{') => self.object(),
            Some('[') => self.array(),
            Some('"') => self.string().map(|_| ()),
            Some('-') | Some('0'..='9') => self.number(),
            Some('t') => self.literal("true"),
            Some('f') => self.literal("false"),
            Some('n') => self.literal("null"),
            _ => Err("INVALID_JSON:value".into()),
        }
    }

    fn object(&mut self) -> Result<(), String> {
        self.bump();
        self.skip_ws();
        let mut keys = Vec::new();
        if self.peek() == Some('}') {
            self.bump();
            return Ok(());
        }
        loop {
            self.skip_ws();
            if self.peek() != Some('"') {
                return Err("INVALID_JSON:object key".into());
            }
            let key = self.string()?;
            if keys.iter().any(|seen| seen == &key) {
                return Err("DUPLICATE_JSON_KEY".into());
            }
            keys.push(key);
            self.skip_ws();
            if self.bump() != Some(':') {
                return Err("INVALID_JSON:colon".into());
            }
            self.value()?;
            self.skip_ws();
            match self.bump() {
                Some('}') => return Ok(()),
                Some(',') => continue,
                _ => return Err("INVALID_JSON:object".into()),
            }
        }
    }

    fn array(&mut self) -> Result<(), String> {
        self.bump();
        self.skip_ws();
        if self.peek() == Some(']') {
            self.bump();
            return Ok(());
        }
        loop {
            self.value()?;
            self.skip_ws();
            match self.bump() {
                Some(']') => return Ok(()),
                Some(',') => continue,
                _ => return Err("INVALID_JSON:array".into()),
            }
        }
    }

    fn string(&mut self) -> Result<String, String> {
        if self.bump() != Some('"') {
            return Err("INVALID_JSON:string".into());
        }
        let mut out = String::new();
        loop {
            match self.bump() {
                Some('"') => return Ok(out),
                Some('\\') => out.push(self.escape()?),
                Some(c) => out.push(c),
                None => return Err("INVALID_JSON:string".into()),
            }
        }
    }

    fn escape(&mut self) -> Result<char, String> {
        match self.bump() {
            Some('"') => Ok('"'),
            Some('\\') => Ok('\\'),
            Some('/') => Ok('/'),
            Some('b') => Ok('\u{0008}'),
            Some('f') => Ok('\u{000c}'),
            Some('n') => Ok('\n'),
            Some('r') => Ok('\r'),
            Some('t') => Ok('\t'),
            Some('u') => {
                let code = self.hex4()?;
                char::from_u32(code).ok_or_else(|| "INVALID_JSON:unicode".to_string())
            }
            _ => Err("INVALID_JSON:escape".into()),
        }
    }

    fn hex4(&mut self) -> Result<u32, String> {
        let mut value = 0u32;
        for _ in 0..4 {
            let c = self.bump().ok_or_else(|| "INVALID_JSON:unicode".to_string())?;
            let digit = c
                .to_digit(16)
                .ok_or_else(|| "INVALID_JSON:unicode".to_string())?;
            value = value * 16 + digit;
        }
        Ok(value)
    }

    fn number(&mut self) -> Result<(), String> {
        if self.peek() == Some('-') {
            self.bump();
        }
        match self.bump() {
            Some('0') => {}
            Some('1'..='9') => while matches!(self.peek(), Some('0'..='9')) {
                self.bump();
            },
            _ => return Err("INVALID_JSON:number".into()),
        }
        if matches!(self.peek(), Some('.') | Some('e') | Some('E')) {
            self.consume_inexact_tail()?;
            if self.deferred.is_none() {
                self.deferred = Some("RAW_INEXACT_JSON_NUMBER".into());
            }
        }
        Ok(())
    }

    fn consume_inexact_tail(&mut self) -> Result<(), String> {
        if self.peek() == Some('.') {
            self.bump();
            if !matches!(self.peek(), Some('0'..='9')) {
                return Err("INVALID_JSON:number".into());
            }
            while matches!(self.peek(), Some('0'..='9')) {
                self.bump();
            }
        }
        if matches!(self.peek(), Some('e') | Some('E')) {
            self.bump();
            if matches!(self.peek(), Some('+') | Some('-')) {
                self.bump();
            }
            if !matches!(self.peek(), Some('0'..='9')) {
                return Err("INVALID_JSON:number".into());
            }
            while matches!(self.peek(), Some('0'..='9')) {
                self.bump();
            }
        }
        Ok(())
    }

    fn literal(&mut self, word: &str) -> Result<(), String> {
        for expected in word.chars() {
            if self.bump() != Some(expected) {
                return Err("INVALID_JSON:literal".into());
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exact_objects_are_admitted_and_inexact_or_duplicate_tokens_are_refused() {
        assert!(admit_exact_json(r#"{"operation":"factor","conductor":8,"coefficients":[["1/1","0/1"]]}"#).is_ok());
        assert!(admit_exact_json(r#"{"note":"1.5e2","n":-2}"#).is_ok());
        assert!(admit_exact_json(r#"{"a":{"a":1},"b":[1,2,null,true]}"#).is_ok());
        assert_eq!(
            admit_exact_json(r#"{"a":1.5}"#),
            Err("RAW_INEXACT_JSON_NUMBER".into())
        );
        assert_eq!(
            admit_exact_json(r#"{"a":0.5,"a":1}"#),
            Err("DUPLICATE_JSON_KEY".into())
        );
        assert_eq!(
            admit_exact_json("{\"a\":1,\"\\u0061\":2}"),
            Err("DUPLICATE_JSON_KEY".into())
        );
    }
}
