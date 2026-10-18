// Lean compiler output
// Module: GaussIntKernel
// Imports: public import Init public meta import Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqGaussInt_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqGaussInt_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqGaussInt(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqGaussInt___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "re"};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "im"};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__16_value;
static lean_once_cell_t lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17;
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprGaussInt_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprGaussInt_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_instReprGaussInt___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_instReprGaussInt_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_instReprGaussInt___closed__0 = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_instReprGaussInt = (const lean_object*)&lp_FiniteQuantum_instReprGaussInt___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_GaussInt_zero___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GaussInt_zero___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_zero;
static lean_once_cell_t lp_FiniteQuantum_GaussInt_one___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GaussInt_one___closed__0;
static lean_once_cell_t lp_FiniteQuantum_GaussInt_one___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GaussInt_one___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_one;
static lean_once_cell_t lp_FiniteQuantum_GaussInt_i___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GaussInt_i___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_i;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_add___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_mul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_mul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_conj(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_sqMod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_sqMod___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqGaussInt_decEq(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
lean_object* v_re_3_; lean_object* v_im_4_; lean_object* v_re_5_; lean_object* v_im_6_; uint8_t v___x_7_; 
v_re_3_ = lean_ctor_get(v_x_1_, 0);
v_im_4_ = lean_ctor_get(v_x_1_, 1);
v_re_5_ = lean_ctor_get(v_x_2_, 0);
v_im_6_ = lean_ctor_get(v_x_2_, 1);
v___x_7_ = lean_int_dec_eq(v_re_3_, v_re_5_);
if (v___x_7_ == 0)
{
return v___x_7_;
}
else
{
uint8_t v___x_8_; 
v___x_8_ = lean_int_dec_eq(v_im_4_, v_im_6_);
return v___x_8_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqGaussInt_decEq___boxed(lean_object* v_x_9_, lean_object* v_x_10_){
_start:
{
uint8_t v_res_11_; lean_object* v_r_12_; 
v_res_11_ = lp_FiniteQuantum_instDecidableEqGaussInt_decEq(v_x_9_, v_x_10_);
lean_dec_ref(v_x_10_);
lean_dec_ref(v_x_9_);
v_r_12_ = lean_box(v_res_11_);
return v_r_12_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqGaussInt(lean_object* v_x_13_, lean_object* v_x_14_){
_start:
{
uint8_t v___x_15_; 
v___x_15_ = lp_FiniteQuantum_instDecidableEqGaussInt_decEq(v_x_13_, v_x_14_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqGaussInt___boxed(lean_object* v_x_16_, lean_object* v_x_17_){
_start:
{
uint8_t v_res_18_; lean_object* v_r_19_; 
v_res_18_ = lp_FiniteQuantum_instDecidableEqGaussInt(v_x_16_, v_x_17_);
lean_dec_ref(v_x_17_);
lean_dec_ref(v_x_16_);
v_r_19_ = lean_box(v_res_18_);
return v_r_19_;
}
}
static lean_object* _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_33_ = lean_unsigned_to_nat(6u);
v___x_34_ = lean_nat_to_int(v___x_33_);
return v___x_34_;
}
}
static lean_object* _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; 
v___x_36_ = ((lean_object*)(lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__0));
v___x_37_ = lean_string_length(v___x_36_);
return v___x_37_;
}
}
static lean_object* _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_38_ = lean_obj_once(&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__9, &lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__9);
v___x_39_ = lean_nat_to_int(v___x_38_);
return v___x_39_;
}
}
static lean_object* _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17(void){
_start:
{
lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_50_ = lean_unsigned_to_nat(0u);
v___x_51_ = lean_nat_to_int(v___x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprGaussInt_repr___redArg(lean_object* v_x_52_){
_start:
{
lean_object* v_re_53_; lean_object* v_im_54_; lean_object* v___x_56_; uint8_t v_isShared_57_; uint8_t v_isSharedCheck_106_; 
v_re_53_ = lean_ctor_get(v_x_52_, 0);
v_im_54_ = lean_ctor_get(v_x_52_, 1);
v_isSharedCheck_106_ = !lean_is_exclusive(v_x_52_);
if (v_isSharedCheck_106_ == 0)
{
v___x_56_ = v_x_52_;
v_isShared_57_ = v_isSharedCheck_106_;
goto v_resetjp_55_;
}
else
{
lean_inc(v_im_54_);
lean_inc(v_re_53_);
lean_dec(v_x_52_);
v___x_56_ = lean_box(0);
v_isShared_57_ = v_isSharedCheck_106_;
goto v_resetjp_55_;
}
v_resetjp_55_:
{
lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___y_62_; uint8_t v___y_63_; lean_object* v___y_64_; lean_object* v___y_78_; lean_object* v___x_98_; lean_object* v___x_99_; uint8_t v___x_100_; 
v___x_58_ = ((lean_object*)(lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__5));
v___x_59_ = ((lean_object*)(lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__6));
v___x_60_ = lean_obj_once(&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__7, &lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__7);
v___x_98_ = lean_unsigned_to_nat(0u);
v___x_99_ = lean_obj_once(&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17, &lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17);
v___x_100_ = lean_int_dec_lt(v_re_53_, v___x_99_);
if (v___x_100_ == 0)
{
lean_object* v___x_101_; lean_object* v___x_102_; 
v___x_101_ = l_Int_repr(v_re_53_);
lean_dec(v_re_53_);
v___x_102_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_102_, 0, v___x_101_);
v___y_78_ = v___x_102_;
goto v___jp_77_;
}
else
{
lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; 
v___x_103_ = l_Int_repr(v_re_53_);
lean_dec(v_re_53_);
v___x_104_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_104_, 0, v___x_103_);
v___x_105_ = l_Repr_addAppParen(v___x_104_, v___x_98_);
v___y_78_ = v___x_105_;
goto v___jp_77_;
}
v___jp_61_:
{
lean_object* v___x_66_; 
if (v_isShared_57_ == 0)
{
lean_ctor_set_tag(v___x_56_, 4);
lean_ctor_set(v___x_56_, 1, v___y_64_);
lean_ctor_set(v___x_56_, 0, v___x_60_);
v___x_66_ = v___x_56_;
goto v_reusejp_65_;
}
else
{
lean_object* v_reuseFailAlloc_76_; 
v_reuseFailAlloc_76_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_76_, 0, v___x_60_);
lean_ctor_set(v_reuseFailAlloc_76_, 1, v___y_64_);
v___x_66_ = v_reuseFailAlloc_76_;
goto v_reusejp_65_;
}
v_reusejp_65_:
{
lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; lean_object* v___x_74_; lean_object* v___x_75_; 
v___x_67_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_67_, 0, v___x_66_);
lean_ctor_set_uint8(v___x_67_, sizeof(void*)*1, v___y_63_);
v___x_68_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_68_, 0, v___y_62_);
lean_ctor_set(v___x_68_, 1, v___x_67_);
v___x_69_ = lean_obj_once(&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__10, &lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__10);
v___x_70_ = ((lean_object*)(lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__11));
v___x_71_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_71_, 0, v___x_70_);
lean_ctor_set(v___x_71_, 1, v___x_68_);
v___x_72_ = ((lean_object*)(lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__12));
v___x_73_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_73_, 0, v___x_71_);
lean_ctor_set(v___x_73_, 1, v___x_72_);
v___x_74_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_74_, 0, v___x_69_);
lean_ctor_set(v___x_74_, 1, v___x_73_);
v___x_75_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_75_, 0, v___x_74_);
lean_ctor_set_uint8(v___x_75_, sizeof(void*)*1, v___y_63_);
return v___x_75_;
}
}
v___jp_77_:
{
lean_object* v___x_79_; uint8_t v___x_80_; lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; lean_object* v___x_84_; lean_object* v___x_85_; lean_object* v___x_86_; lean_object* v___x_87_; lean_object* v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; lean_object* v___x_91_; uint8_t v___x_92_; 
v___x_79_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_79_, 0, v___x_60_);
lean_ctor_set(v___x_79_, 1, v___y_78_);
v___x_80_ = 0;
v___x_81_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_81_, 0, v___x_79_);
lean_ctor_set_uint8(v___x_81_, sizeof(void*)*1, v___x_80_);
v___x_82_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_82_, 0, v___x_59_);
lean_ctor_set(v___x_82_, 1, v___x_81_);
v___x_83_ = ((lean_object*)(lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__14));
v___x_84_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_84_, 0, v___x_82_);
lean_ctor_set(v___x_84_, 1, v___x_83_);
v___x_85_ = lean_box(1);
v___x_86_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_86_, 0, v___x_84_);
lean_ctor_set(v___x_86_, 1, v___x_85_);
v___x_87_ = ((lean_object*)(lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__16));
v___x_88_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_88_, 0, v___x_86_);
lean_ctor_set(v___x_88_, 1, v___x_87_);
v___x_89_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_89_, 0, v___x_88_);
lean_ctor_set(v___x_89_, 1, v___x_58_);
v___x_90_ = lean_unsigned_to_nat(0u);
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17, &lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17);
v___x_92_ = lean_int_dec_lt(v_im_54_, v___x_91_);
if (v___x_92_ == 0)
{
lean_object* v___x_93_; lean_object* v___x_94_; 
v___x_93_ = l_Int_repr(v_im_54_);
lean_dec(v_im_54_);
v___x_94_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_94_, 0, v___x_93_);
v___y_62_ = v___x_89_;
v___y_63_ = v___x_80_;
v___y_64_ = v___x_94_;
goto v___jp_61_;
}
else
{
lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; 
v___x_95_ = l_Int_repr(v_im_54_);
lean_dec(v_im_54_);
v___x_96_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_96_, 0, v___x_95_);
v___x_97_ = l_Repr_addAppParen(v___x_96_, v___x_90_);
v___y_62_ = v___x_89_;
v___y_63_ = v___x_80_;
v___y_64_ = v___x_97_;
goto v___jp_61_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprGaussInt_repr(lean_object* v_x_107_, lean_object* v_prec_108_){
_start:
{
lean_object* v___x_109_; 
v___x_109_ = lp_FiniteQuantum_instReprGaussInt_repr___redArg(v_x_107_);
return v___x_109_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprGaussInt_repr___boxed(lean_object* v_x_110_, lean_object* v_prec_111_){
_start:
{
lean_object* v_res_112_; 
v_res_112_ = lp_FiniteQuantum_instReprGaussInt_repr(v_x_110_, v_prec_111_);
lean_dec(v_prec_111_);
return v_res_112_;
}
}
static lean_object* _init_lp_FiniteQuantum_GaussInt_zero___closed__0(void){
_start:
{
lean_object* v___x_115_; lean_object* v___x_116_; 
v___x_115_ = lean_obj_once(&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17, &lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17);
v___x_116_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_116_, 0, v___x_115_);
lean_ctor_set(v___x_116_, 1, v___x_115_);
return v___x_116_;
}
}
static lean_object* _init_lp_FiniteQuantum_GaussInt_zero(void){
_start:
{
lean_object* v___x_117_; 
v___x_117_ = lean_obj_once(&lp_FiniteQuantum_GaussInt_zero___closed__0, &lp_FiniteQuantum_GaussInt_zero___closed__0_once, _init_lp_FiniteQuantum_GaussInt_zero___closed__0);
return v___x_117_;
}
}
static lean_object* _init_lp_FiniteQuantum_GaussInt_one___closed__0(void){
_start:
{
lean_object* v___x_118_; lean_object* v___x_119_; 
v___x_118_ = lean_unsigned_to_nat(1u);
v___x_119_ = lean_nat_to_int(v___x_118_);
return v___x_119_;
}
}
static lean_object* _init_lp_FiniteQuantum_GaussInt_one___closed__1(void){
_start:
{
lean_object* v___x_120_; lean_object* v___x_121_; lean_object* v___x_122_; 
v___x_120_ = lean_obj_once(&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17, &lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17);
v___x_121_ = lean_obj_once(&lp_FiniteQuantum_GaussInt_one___closed__0, &lp_FiniteQuantum_GaussInt_one___closed__0_once, _init_lp_FiniteQuantum_GaussInt_one___closed__0);
v___x_122_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_122_, 0, v___x_121_);
lean_ctor_set(v___x_122_, 1, v___x_120_);
return v___x_122_;
}
}
static lean_object* _init_lp_FiniteQuantum_GaussInt_one(void){
_start:
{
lean_object* v___x_123_; 
v___x_123_ = lean_obj_once(&lp_FiniteQuantum_GaussInt_one___closed__1, &lp_FiniteQuantum_GaussInt_one___closed__1_once, _init_lp_FiniteQuantum_GaussInt_one___closed__1);
return v___x_123_;
}
}
static lean_object* _init_lp_FiniteQuantum_GaussInt_i___closed__0(void){
_start:
{
lean_object* v___x_124_; lean_object* v___x_125_; lean_object* v___x_126_; 
v___x_124_ = lean_obj_once(&lp_FiniteQuantum_GaussInt_one___closed__0, &lp_FiniteQuantum_GaussInt_one___closed__0_once, _init_lp_FiniteQuantum_GaussInt_one___closed__0);
v___x_125_ = lean_obj_once(&lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17, &lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_instReprGaussInt_repr___redArg___closed__17);
v___x_126_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_126_, 0, v___x_125_);
lean_ctor_set(v___x_126_, 1, v___x_124_);
return v___x_126_;
}
}
static lean_object* _init_lp_FiniteQuantum_GaussInt_i(void){
_start:
{
lean_object* v___x_127_; 
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_GaussInt_i___closed__0, &lp_FiniteQuantum_GaussInt_i___closed__0_once, _init_lp_FiniteQuantum_GaussInt_i___closed__0);
return v___x_127_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_add(lean_object* v_a_128_, lean_object* v_b_129_){
_start:
{
lean_object* v_re_130_; lean_object* v_im_131_; lean_object* v_re_132_; lean_object* v_im_133_; lean_object* v___x_135_; uint8_t v_isShared_136_; uint8_t v_isSharedCheck_142_; 
v_re_130_ = lean_ctor_get(v_a_128_, 0);
v_im_131_ = lean_ctor_get(v_a_128_, 1);
v_re_132_ = lean_ctor_get(v_b_129_, 0);
v_im_133_ = lean_ctor_get(v_b_129_, 1);
v_isSharedCheck_142_ = !lean_is_exclusive(v_b_129_);
if (v_isSharedCheck_142_ == 0)
{
v___x_135_ = v_b_129_;
v_isShared_136_ = v_isSharedCheck_142_;
goto v_resetjp_134_;
}
else
{
lean_inc(v_im_133_);
lean_inc(v_re_132_);
lean_dec(v_b_129_);
v___x_135_ = lean_box(0);
v_isShared_136_ = v_isSharedCheck_142_;
goto v_resetjp_134_;
}
v_resetjp_134_:
{
lean_object* v___x_137_; lean_object* v___x_138_; lean_object* v___x_140_; 
v___x_137_ = lean_int_add(v_re_130_, v_re_132_);
lean_dec(v_re_132_);
v___x_138_ = lean_int_add(v_im_131_, v_im_133_);
lean_dec(v_im_133_);
if (v_isShared_136_ == 0)
{
lean_ctor_set(v___x_135_, 1, v___x_138_);
lean_ctor_set(v___x_135_, 0, v___x_137_);
v___x_140_ = v___x_135_;
goto v_reusejp_139_;
}
else
{
lean_object* v_reuseFailAlloc_141_; 
v_reuseFailAlloc_141_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_141_, 0, v___x_137_);
lean_ctor_set(v_reuseFailAlloc_141_, 1, v___x_138_);
v___x_140_ = v_reuseFailAlloc_141_;
goto v_reusejp_139_;
}
v_reusejp_139_:
{
return v___x_140_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_add___boxed(lean_object* v_a_143_, lean_object* v_b_144_){
_start:
{
lean_object* v_res_145_; 
v_res_145_ = lp_FiniteQuantum_GaussInt_add(v_a_143_, v_b_144_);
lean_dec_ref(v_a_143_);
return v_res_145_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_neg(lean_object* v_a_146_){
_start:
{
lean_object* v_re_147_; lean_object* v_im_148_; lean_object* v___x_150_; uint8_t v_isShared_151_; uint8_t v_isSharedCheck_157_; 
v_re_147_ = lean_ctor_get(v_a_146_, 0);
v_im_148_ = lean_ctor_get(v_a_146_, 1);
v_isSharedCheck_157_ = !lean_is_exclusive(v_a_146_);
if (v_isSharedCheck_157_ == 0)
{
v___x_150_ = v_a_146_;
v_isShared_151_ = v_isSharedCheck_157_;
goto v_resetjp_149_;
}
else
{
lean_inc(v_im_148_);
lean_inc(v_re_147_);
lean_dec(v_a_146_);
v___x_150_ = lean_box(0);
v_isShared_151_ = v_isSharedCheck_157_;
goto v_resetjp_149_;
}
v_resetjp_149_:
{
lean_object* v___x_152_; lean_object* v___x_153_; lean_object* v___x_155_; 
v___x_152_ = lean_int_neg(v_re_147_);
lean_dec(v_re_147_);
v___x_153_ = lean_int_neg(v_im_148_);
lean_dec(v_im_148_);
if (v_isShared_151_ == 0)
{
lean_ctor_set(v___x_150_, 1, v___x_153_);
lean_ctor_set(v___x_150_, 0, v___x_152_);
v___x_155_ = v___x_150_;
goto v_reusejp_154_;
}
else
{
lean_object* v_reuseFailAlloc_156_; 
v_reuseFailAlloc_156_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_156_, 0, v___x_152_);
lean_ctor_set(v_reuseFailAlloc_156_, 1, v___x_153_);
v___x_155_ = v_reuseFailAlloc_156_;
goto v_reusejp_154_;
}
v_reusejp_154_:
{
return v___x_155_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_mul(lean_object* v_a_158_, lean_object* v_b_159_){
_start:
{
lean_object* v_re_160_; lean_object* v_im_161_; lean_object* v_re_162_; lean_object* v_im_163_; lean_object* v___x_165_; uint8_t v_isShared_166_; uint8_t v_isSharedCheck_176_; 
v_re_160_ = lean_ctor_get(v_a_158_, 0);
v_im_161_ = lean_ctor_get(v_a_158_, 1);
v_re_162_ = lean_ctor_get(v_b_159_, 0);
v_im_163_ = lean_ctor_get(v_b_159_, 1);
v_isSharedCheck_176_ = !lean_is_exclusive(v_b_159_);
if (v_isSharedCheck_176_ == 0)
{
v___x_165_ = v_b_159_;
v_isShared_166_ = v_isSharedCheck_176_;
goto v_resetjp_164_;
}
else
{
lean_inc(v_im_163_);
lean_inc(v_re_162_);
lean_dec(v_b_159_);
v___x_165_ = lean_box(0);
v_isShared_166_ = v_isSharedCheck_176_;
goto v_resetjp_164_;
}
v_resetjp_164_:
{
lean_object* v___x_167_; lean_object* v___x_168_; lean_object* v___x_169_; lean_object* v___x_170_; lean_object* v___x_171_; lean_object* v___x_172_; lean_object* v___x_174_; 
v___x_167_ = lean_int_mul(v_re_160_, v_re_162_);
v___x_168_ = lean_int_mul(v_im_161_, v_im_163_);
v___x_169_ = lean_int_sub(v___x_167_, v___x_168_);
lean_dec(v___x_168_);
lean_dec(v___x_167_);
v___x_170_ = lean_int_mul(v_re_160_, v_im_163_);
lean_dec(v_im_163_);
v___x_171_ = lean_int_mul(v_im_161_, v_re_162_);
lean_dec(v_re_162_);
v___x_172_ = lean_int_add(v___x_170_, v___x_171_);
lean_dec(v___x_171_);
lean_dec(v___x_170_);
if (v_isShared_166_ == 0)
{
lean_ctor_set(v___x_165_, 1, v___x_172_);
lean_ctor_set(v___x_165_, 0, v___x_169_);
v___x_174_ = v___x_165_;
goto v_reusejp_173_;
}
else
{
lean_object* v_reuseFailAlloc_175_; 
v_reuseFailAlloc_175_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_175_, 0, v___x_169_);
lean_ctor_set(v_reuseFailAlloc_175_, 1, v___x_172_);
v___x_174_ = v_reuseFailAlloc_175_;
goto v_reusejp_173_;
}
v_reusejp_173_:
{
return v___x_174_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_mul___boxed(lean_object* v_a_177_, lean_object* v_b_178_){
_start:
{
lean_object* v_res_179_; 
v_res_179_ = lp_FiniteQuantum_GaussInt_mul(v_a_177_, v_b_178_);
lean_dec_ref(v_a_177_);
return v_res_179_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_conj(lean_object* v_a_180_){
_start:
{
lean_object* v_re_181_; lean_object* v_im_182_; lean_object* v___x_184_; uint8_t v_isShared_185_; uint8_t v_isSharedCheck_190_; 
v_re_181_ = lean_ctor_get(v_a_180_, 0);
v_im_182_ = lean_ctor_get(v_a_180_, 1);
v_isSharedCheck_190_ = !lean_is_exclusive(v_a_180_);
if (v_isSharedCheck_190_ == 0)
{
v___x_184_ = v_a_180_;
v_isShared_185_ = v_isSharedCheck_190_;
goto v_resetjp_183_;
}
else
{
lean_inc(v_im_182_);
lean_inc(v_re_181_);
lean_dec(v_a_180_);
v___x_184_ = lean_box(0);
v_isShared_185_ = v_isSharedCheck_190_;
goto v_resetjp_183_;
}
v_resetjp_183_:
{
lean_object* v___x_186_; lean_object* v___x_188_; 
v___x_186_ = lean_int_neg(v_im_182_);
lean_dec(v_im_182_);
if (v_isShared_185_ == 0)
{
lean_ctor_set(v___x_184_, 1, v___x_186_);
v___x_188_ = v___x_184_;
goto v_reusejp_187_;
}
else
{
lean_object* v_reuseFailAlloc_189_; 
v_reuseFailAlloc_189_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_189_, 0, v_re_181_);
lean_ctor_set(v_reuseFailAlloc_189_, 1, v___x_186_);
v___x_188_ = v_reuseFailAlloc_189_;
goto v_reusejp_187_;
}
v_reusejp_187_:
{
return v___x_188_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_sqMod(lean_object* v_a_191_){
_start:
{
lean_object* v_re_192_; lean_object* v_im_193_; lean_object* v___x_194_; lean_object* v___x_195_; lean_object* v___x_196_; 
v_re_192_ = lean_ctor_get(v_a_191_, 0);
v_im_193_ = lean_ctor_get(v_a_191_, 1);
v___x_194_ = lean_int_mul(v_re_192_, v_re_192_);
v___x_195_ = lean_int_mul(v_im_193_, v_im_193_);
v___x_196_ = lean_int_add(v___x_194_, v___x_195_);
lean_dec(v___x_195_);
lean_dec(v___x_194_);
return v___x_196_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GaussInt_sqMod___boxed(lean_object* v_a_197_){
_start:
{
lean_object* v_res_198_; 
v_res_198_ = lp_FiniteQuantum_GaussInt_sqMod(v_a_197_);
lean_dec_ref(v_a_197_);
return v_res_198_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_GaussIntKernel(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_GaussInt_zero = _init_lp_FiniteQuantum_GaussInt_zero();
lean_mark_persistent(lp_FiniteQuantum_GaussInt_zero);
lp_FiniteQuantum_GaussInt_one = _init_lp_FiniteQuantum_GaussInt_one();
lean_mark_persistent(lp_FiniteQuantum_GaussInt_one);
lp_FiniteQuantum_GaussInt_i = _init_lp_FiniteQuantum_GaussInt_i();
lean_mark_persistent(lp_FiniteQuantum_GaussInt_i);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
