//! Distinct global-incidence and zero-sum-local overlap maps, exact over F2.
#[derive(Debug,Clone,PartialEq,Eq)]
pub struct Certificate {
 pub incidence:Vec<Vec<u8>>, pub overlaps:Vec<Vec<usize>>, pub local_dimension:usize,
 pub delta0:Vec<Vec<u8>>, pub discrepancy:Vec<u8>, pub incidence_rank:usize,
 pub incidence_augmented_rank:usize, pub delta0_rank:usize, pub delta0_augmented_rank:usize,
 pub h1_dimension:usize, pub character_on_columns:Vec<u8>,pub obstruction_pairing:u8,
 pub global_section:Option<Vec<u8>>,
}
pub fn rank(rows:&[Vec<u8>],columns:usize)->Result<usize,&'static str>{
 if rows.iter().any(|r|r.len()!=columns || r.iter().any(|&x|x>1)){return Err("binary rectangular matrix required");}
 let mut a=rows.to_vec();let mut k=0;
 for j in 0..columns {if let Some(i)=(k..a.len()).find(|&i|a[i][j]==1){a.swap(i,k);for i in k+1..a.len(){if a[i][j]==1{for u in j..columns{a[i][u]^=a[k][u];}}}k+=1;}}
 Ok(k)
}
pub fn certify(n:usize,contexts:&[Vec<usize>],targets:&[u8])->Result<Certificate,&'static str>{
 if n==0 || contexts.is_empty() || contexts.len()!=targets.len() || targets.iter().any(|&x|x>1){return Err("nonempty binary context system required");}
 for c in contexts {let mut copy=c.clone();copy.sort();copy.dedup();if c.len()<2 || copy.len()!=c.len() || c.iter().any(|&r|r>=n){return Err("distinct in-range context variables required");}}
 if (0..n).any(|r|contexts.iter().filter(|c|c.contains(&r)).count()!=2){return Err("degree-two cover required");}
 let mut offsets=vec![0];for c in contexts{offsets.push(offsets.last().unwrap()+c.len()-1);}let dim=*offsets.last().unwrap();
 let mut overlaps=vec![];let mut delta0=vec![];let mut discrepancy=vec![];
 for i in 0..contexts.len(){for j in i+1..contexts.len(){let mut common:Vec<_>=contexts[i].iter().filter(|r|contexts[j].contains(r)).copied().collect();common.sort();for r in common{
  overlaps.push(vec![i,j,r]);let mut row=vec![0;dim];let mut b=0;
  for k in [i,j]{let pos=contexts[k].iter().position(|&x|x==r).unwrap();for u in 1..contexts[k].len(){if pos==0 || pos==u{row[offsets[k]+u-1]^=1;}}if pos==0{b^=targets[k];}}
  delta0.push(row);discrepancy.push(b);
 }}}
 let incidence:Vec<Vec<u8>>=contexts.iter().map(|c|(0..n).map(|r|u8::from(c.contains(&r))).collect()).collect();
 let aug=|a:&[Vec<u8>],b:&[u8]|->Vec<Vec<u8>>{a.iter().zip(b).map(|(r,&b)|{let mut x=r.clone();x.push(b);x}).collect()};
 let ri=rank(&incidence,n)?;let ria=rank(&aug(&incidence,targets),n+1)?;let rd=rank(&delta0,dim)?;let ra=rank(&aug(&delta0,&discrepancy),dim+1)?;
 let character_on_columns:Vec<_>=(0..dim).map(|j|delta0.iter().fold(0,|a,r|a^r[j])).collect();
 if character_on_columns.iter().any(|&x|x!=0){return Err("character does not annihilate image");}
 let obstruction_pairing=discrepancy.iter().fold(0,|a,&b|a^b);
 let mut a=aug(&incidence,targets);let mut pivots=vec![];let mut k=0;
 for j in 0..n{if let Some(i)=(k..a.len()).find(|&i|a[i][j]==1){a.swap(i,k);for i in 0..a.len(){if i!=k && a[i][j]==1{for u in j..=n{a[i][u]^=a[k][u];}}}pivots.push(j);k+=1;}}
 let global_section=if a.iter().any(|r|r[..n].iter().all(|&x|x==0)&&r[n]==1){None}else{let mut g=vec![0;n];for (i,&j) in pivots.iter().enumerate(){g[j]=a[i][n];}Some(g)};
 Ok(Certificate{incidence,overlaps,local_dimension:dim,delta0,discrepancy,incidence_rank:ri,incidence_augmented_rank:ria,delta0_rank:rd,delta0_augmented_rank:ra,h1_dimension:n-rd,character_on_columns,obstruction_pairing,global_section})
}
#[cfg(test)]mod tests{use super::*;fn m()->Vec<Vec<usize>>{vec![vec![0,1,2],vec![3,4,5],vec![6,7,8],vec![0,3,6],vec![1,4,7],vec![2,5,8]]}
 #[test]fn maps_have_different_ranks(){let c=certify(9,&m(),&[0,0,0,0,0,1]).unwrap();assert_eq!((c.incidence_rank,c.delta0_rank,c.delta0_augmented_rank),(5,8,9));assert_eq!(c.obstruction_pairing,1);}
 #[test]fn actual_zero_section_control(){let c=certify(9,&m(),&[0;6]).unwrap();assert_eq!(c.global_section,Some(vec![0;9]));assert_eq!(c.obstruction_pairing,0);assert_eq!(c.delta0_rank,c.delta0_augmented_rank);}
 #[test]fn malformed_cover_refused(){let mut c=m();c[0][0]=1;assert!(certify(9,&c,&[0;6]).is_err());assert!(rank(&[vec![2]],1).is_err());}
}
