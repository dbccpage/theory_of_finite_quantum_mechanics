// Lean compiler output
// Module: MeronCharacter
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
lean_object* l_List_reverse___redArg(lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* l_instBEqOfDecidableEq___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*);
uint8_t l_List_elem___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* l_List_lengthTR___redArg(lean_object*);
lean_object* l_Int_pow(lean_object*, lean_object*);
lean_object* l_List_appendTR___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_List_mapTR_loop___at___00MeronCharacter_orbitSigns_spec__0(uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_List_mapTR_loop___at___00MeronCharacter_orbitSigns_spec__0___boxed(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_po023_MeronCharacter_orbitSigns___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_po023_MeronCharacter_orbitSigns___closed__0;
static lean_once_cell_t lp_po023_MeronCharacter_orbitSigns___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_po023_MeronCharacter_orbitSigns___closed__1;
LEAN_EXPORT lean_object* lp_po023_MeronCharacter_orbitSigns(lean_object*);
LEAN_EXPORT lean_object* lp_po023_MeronCharacter_orbitSigns___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023___private_MeronCharacter_0__MeronCharacter_orbitSigns_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023___private_MeronCharacter_0__MeronCharacter_orbitSigns_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_po023_MeronCharacter_compressedSum___lam__0(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_po023_MeronCharacter_compressedSum___lam__0___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_po023_MeronCharacter_compressedSum___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_po023_MeronCharacter_compressedSum___lam__0___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_po023_MeronCharacter_compressedSum___closed__0 = (const lean_object*)&lp_po023_MeronCharacter_compressedSum___closed__0_value;
static const lean_closure_object lp_po023_MeronCharacter_compressedSum___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*1, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_instBEqOfDecidableEq___redArg___lam__0___boxed, .m_arity = 3, .m_num_fixed = 1, .m_objs = {((lean_object*)&lp_po023_MeronCharacter_compressedSum___closed__0_value)} };
static const lean_object* lp_po023_MeronCharacter_compressedSum___closed__1 = (const lean_object*)&lp_po023_MeronCharacter_compressedSum___closed__1_value;
static lean_once_cell_t lp_po023_MeronCharacter_compressedSum___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_po023_MeronCharacter_compressedSum___closed__2;
static lean_once_cell_t lp_po023_MeronCharacter_compressedSum___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_po023_MeronCharacter_compressedSum___closed__3;
LEAN_EXPORT lean_object* lp_po023_MeronCharacter_compressedSum(lean_object*);
LEAN_EXPORT lean_object* lp_po023_List_mapTR_loop___at___00MeronCharacter_orbitSigns_spec__0(uint8_t v_head_1_, lean_object* v_a_2_, lean_object* v_a_3_){
_start:
{
if (lean_obj_tag(v_a_2_) == 0)
{
lean_object* v___x_4_; 
v___x_4_ = l_List_reverse___redArg(v_a_3_);
return v___x_4_;
}
else
{
lean_object* v_head_5_; lean_object* v_tail_6_; lean_object* v___x_8_; uint8_t v_isShared_9_; uint8_t v_isSharedCheck_17_; 
v_head_5_ = lean_ctor_get(v_a_2_, 0);
v_tail_6_ = lean_ctor_get(v_a_2_, 1);
v_isSharedCheck_17_ = !lean_is_exclusive(v_a_2_);
if (v_isSharedCheck_17_ == 0)
{
v___x_8_ = v_a_2_;
v_isShared_9_ = v_isSharedCheck_17_;
goto v_resetjp_7_;
}
else
{
lean_inc(v_tail_6_);
lean_inc(v_head_5_);
lean_dec(v_a_2_);
v___x_8_ = lean_box(0);
v_isShared_9_ = v_isSharedCheck_17_;
goto v_resetjp_7_;
}
v_resetjp_7_:
{
lean_object* v___y_11_; 
if (v_head_1_ == 0)
{
v___y_11_ = v_head_5_;
goto v___jp_10_;
}
else
{
lean_object* v___x_16_; 
v___x_16_ = lean_int_neg(v_head_5_);
lean_dec(v_head_5_);
v___y_11_ = v___x_16_;
goto v___jp_10_;
}
v___jp_10_:
{
lean_object* v___x_13_; 
if (v_isShared_9_ == 0)
{
lean_ctor_set(v___x_8_, 1, v_a_3_);
lean_ctor_set(v___x_8_, 0, v___y_11_);
v___x_13_ = v___x_8_;
goto v_reusejp_12_;
}
else
{
lean_object* v_reuseFailAlloc_15_; 
v_reuseFailAlloc_15_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_15_, 0, v___y_11_);
lean_ctor_set(v_reuseFailAlloc_15_, 1, v_a_3_);
v___x_13_ = v_reuseFailAlloc_15_;
goto v_reusejp_12_;
}
v_reusejp_12_:
{
v_a_2_ = v_tail_6_;
v_a_3_ = v___x_13_;
goto _start;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_po023_List_mapTR_loop___at___00MeronCharacter_orbitSigns_spec__0___boxed(lean_object* v_head_18_, lean_object* v_a_19_, lean_object* v_a_20_){
_start:
{
uint8_t v_head_101__boxed_21_; lean_object* v_res_22_; 
v_head_101__boxed_21_ = lean_unbox(v_head_18_);
v_res_22_ = lp_po023_List_mapTR_loop___at___00MeronCharacter_orbitSigns_spec__0(v_head_101__boxed_21_, v_a_19_, v_a_20_);
return v_res_22_;
}
}
static lean_object* _init_lp_po023_MeronCharacter_orbitSigns___closed__0(void){
_start:
{
lean_object* v___x_23_; lean_object* v___x_24_; 
v___x_23_ = lean_unsigned_to_nat(1u);
v___x_24_ = lean_nat_to_int(v___x_23_);
return v___x_24_;
}
}
static lean_object* _init_lp_po023_MeronCharacter_orbitSigns___closed__1(void){
_start:
{
lean_object* v___x_25_; lean_object* v___x_26_; lean_object* v___x_27_; 
v___x_25_ = lean_box(0);
v___x_26_ = lean_obj_once(&lp_po023_MeronCharacter_orbitSigns___closed__0, &lp_po023_MeronCharacter_orbitSigns___closed__0_once, _init_lp_po023_MeronCharacter_orbitSigns___closed__0);
v___x_27_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_27_, 0, v___x_26_);
lean_ctor_set(v___x_27_, 1, v___x_25_);
return v___x_27_;
}
}
LEAN_EXPORT lean_object* lp_po023_MeronCharacter_orbitSigns(lean_object* v_x_28_){
_start:
{
if (lean_obj_tag(v_x_28_) == 0)
{
lean_object* v___x_29_; 
v___x_29_ = lean_obj_once(&lp_po023_MeronCharacter_orbitSigns___closed__1, &lp_po023_MeronCharacter_orbitSigns___closed__1_once, _init_lp_po023_MeronCharacter_orbitSigns___closed__1);
return v___x_29_;
}
else
{
lean_object* v_head_30_; lean_object* v_tail_31_; lean_object* v___x_32_; lean_object* v___x_33_; uint8_t v___x_34_; lean_object* v___x_35_; lean_object* v___x_36_; 
v_head_30_ = lean_ctor_get(v_x_28_, 0);
v_tail_31_ = lean_ctor_get(v_x_28_, 1);
v___x_32_ = lp_po023_MeronCharacter_orbitSigns(v_tail_31_);
v___x_33_ = lean_box(0);
v___x_34_ = lean_unbox(v_head_30_);
lean_inc(v___x_32_);
v___x_35_ = lp_po023_List_mapTR_loop___at___00MeronCharacter_orbitSigns_spec__0(v___x_34_, v___x_32_, v___x_33_);
v___x_36_ = l_List_appendTR___redArg(v___x_32_, v___x_35_);
return v___x_36_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_MeronCharacter_orbitSigns___boxed(lean_object* v_x_37_){
_start:
{
lean_object* v_res_38_; 
v_res_38_ = lp_po023_MeronCharacter_orbitSigns(v_x_37_);
lean_dec(v_x_37_);
return v_res_38_;
}
}
LEAN_EXPORT lean_object* lp_po023___private_MeronCharacter_0__MeronCharacter_orbitSigns_match__1_splitter___redArg(lean_object* v_x_39_, lean_object* v_h__1_40_, lean_object* v_h__2_41_){
_start:
{
if (lean_obj_tag(v_x_39_) == 0)
{
lean_object* v___x_42_; lean_object* v___x_43_; 
lean_dec(v_h__2_41_);
v___x_42_ = lean_box(0);
v___x_43_ = lean_apply_1(v_h__1_40_, v___x_42_);
return v___x_43_;
}
else
{
lean_object* v_head_44_; lean_object* v_tail_45_; lean_object* v___x_46_; 
lean_dec(v_h__1_40_);
v_head_44_ = lean_ctor_get(v_x_39_, 0);
lean_inc(v_head_44_);
v_tail_45_ = lean_ctor_get(v_x_39_, 1);
lean_inc(v_tail_45_);
lean_dec_ref_known(v_x_39_, 2);
v___x_46_ = lean_apply_2(v_h__2_41_, v_head_44_, v_tail_45_);
return v___x_46_;
}
}
}
LEAN_EXPORT lean_object* lp_po023___private_MeronCharacter_0__MeronCharacter_orbitSigns_match__1_splitter(lean_object* v_motive_47_, lean_object* v_x_48_, lean_object* v_h__1_49_, lean_object* v_h__2_50_){
_start:
{
if (lean_obj_tag(v_x_48_) == 0)
{
lean_object* v___x_51_; lean_object* v___x_52_; 
lean_dec(v_h__2_50_);
v___x_51_ = lean_box(0);
v___x_52_ = lean_apply_1(v_h__1_49_, v___x_51_);
return v___x_52_;
}
else
{
lean_object* v_head_53_; lean_object* v_tail_54_; lean_object* v___x_55_; 
lean_dec(v_h__1_49_);
v_head_53_ = lean_ctor_get(v_x_48_, 0);
lean_inc(v_head_53_);
v_tail_54_ = lean_ctor_get(v_x_48_, 1);
lean_inc(v_tail_54_);
lean_dec_ref_known(v_x_48_, 2);
v___x_55_ = lean_apply_2(v_h__2_50_, v_head_53_, v_tail_54_);
return v___x_55_;
}
}
}
LEAN_EXPORT uint8_t lp_po023_MeronCharacter_compressedSum___lam__0(uint8_t v___y_56_, uint8_t v___y_57_){
_start:
{
if (v___y_56_ == 0)
{
if (v___y_57_ == 0)
{
uint8_t v___x_58_; 
v___x_58_ = 1;
return v___x_58_;
}
else
{
return v___y_56_;
}
}
else
{
return v___y_57_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_MeronCharacter_compressedSum___lam__0___boxed(lean_object* v___y_59_, lean_object* v___y_60_){
_start:
{
uint8_t v___y_51__boxed_61_; uint8_t v___y_52__boxed_62_; uint8_t v_res_63_; lean_object* v_r_64_; 
v___y_51__boxed_61_ = lean_unbox(v___y_59_);
v___y_52__boxed_62_ = lean_unbox(v___y_60_);
v_res_63_ = lp_po023_MeronCharacter_compressedSum___lam__0(v___y_51__boxed_61_, v___y_52__boxed_62_);
v_r_64_ = lean_box(v_res_63_);
return v_r_64_;
}
}
static lean_object* _init_lp_po023_MeronCharacter_compressedSum___closed__2(void){
_start:
{
lean_object* v___x_68_; lean_object* v___x_69_; 
v___x_68_ = lean_unsigned_to_nat(2u);
v___x_69_ = lean_nat_to_int(v___x_68_);
return v___x_69_;
}
}
static lean_object* _init_lp_po023_MeronCharacter_compressedSum___closed__3(void){
_start:
{
lean_object* v___x_70_; lean_object* v___x_71_; 
v___x_70_ = lean_unsigned_to_nat(0u);
v___x_71_ = lean_nat_to_int(v___x_70_);
return v___x_71_;
}
}
LEAN_EXPORT lean_object* lp_po023_MeronCharacter_compressedSum(lean_object* v_flags_72_){
_start:
{
lean_object* v___f_73_; uint8_t v___x_74_; lean_object* v___x_75_; uint8_t v___x_76_; 
v___f_73_ = ((lean_object*)(lp_po023_MeronCharacter_compressedSum___closed__1));
v___x_74_ = 1;
v___x_75_ = lean_box(v___x_74_);
lean_inc(v_flags_72_);
v___x_76_ = l_List_elem___redArg(v___f_73_, v___x_75_, v_flags_72_);
if (v___x_76_ == 0)
{
lean_object* v___x_77_; lean_object* v___x_78_; lean_object* v___x_79_; 
v___x_77_ = lean_obj_once(&lp_po023_MeronCharacter_compressedSum___closed__2, &lp_po023_MeronCharacter_compressedSum___closed__2_once, _init_lp_po023_MeronCharacter_compressedSum___closed__2);
v___x_78_ = l_List_lengthTR___redArg(v_flags_72_);
lean_dec(v_flags_72_);
v___x_79_ = l_Int_pow(v___x_77_, v___x_78_);
lean_dec(v___x_78_);
return v___x_79_;
}
else
{
lean_object* v___x_80_; 
lean_dec(v_flags_72_);
v___x_80_ = lean_obj_once(&lp_po023_MeronCharacter_compressedSum___closed__3, &lp_po023_MeronCharacter_compressedSum___closed__3_once, _init_lp_po023_MeronCharacter_compressedSum___closed__3);
return v___x_80_;
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
void lean_initialize_runtime_module();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_po023_MeronCharacter(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
lean_initialize_runtime_module();
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
