// Lean compiler output
// Module: Expressivity
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
uint8_t lean_usize_dec_eq(size_t, size_t);
size_t lean_usize_sub(size_t, size_t);
lean_object* lean_array_uget_borrowed(lean_object*, size_t);
lean_object* lean_nat_abs(lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* lean_array_mk(lean_object*);
lean_object* lean_array_get_size(lean_object*);
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
size_t lean_usize_of_nat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0_spec__0(lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_SymbolGame_expressivityNorm(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0_spec__0(lean_object* v_as_1_, size_t v_i_2_, size_t v_stop_3_, lean_object* v_b_4_){
_start:
{
uint8_t v___x_5_; 
v___x_5_ = lean_usize_dec_eq(v_i_2_, v_stop_3_);
if (v___x_5_ == 0)
{
size_t v___x_6_; size_t v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v___x_6_ = ((size_t)1ULL);
v___x_7_ = lean_usize_sub(v_i_2_, v___x_6_);
v___x_8_ = lean_array_uget_borrowed(v_as_1_, v___x_7_);
v___x_9_ = lean_nat_abs(v___x_8_);
v___x_10_ = lean_nat_add(v___x_9_, v_b_4_);
lean_dec(v_b_4_);
lean_dec(v___x_9_);
v_i_2_ = v___x_7_;
v_b_4_ = v___x_10_;
goto _start;
}
else
{
return v_b_4_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0_spec__0___boxed(lean_object* v_as_12_, lean_object* v_i_13_, lean_object* v_stop_14_, lean_object* v_b_15_){
_start:
{
size_t v_i_boxed_16_; size_t v_stop_boxed_17_; lean_object* v_res_18_; 
v_i_boxed_16_ = lean_unbox_usize(v_i_13_);
lean_dec(v_i_13_);
v_stop_boxed_17_ = lean_unbox_usize(v_stop_14_);
lean_dec(v_stop_14_);
v_res_18_ = lp_FiniteQuantum___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0_spec__0(v_as_12_, v_i_boxed_16_, v_stop_boxed_17_, v_b_15_);
lean_dec_ref(v_as_12_);
return v_res_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0(lean_object* v_init_19_, lean_object* v_l_20_){
_start:
{
lean_object* v___x_21_; lean_object* v___x_22_; lean_object* v___x_23_; uint8_t v___x_24_; 
v___x_21_ = lean_array_mk(v_l_20_);
v___x_22_ = lean_array_get_size(v___x_21_);
v___x_23_ = lean_unsigned_to_nat(0u);
v___x_24_ = lean_nat_dec_lt(v___x_23_, v___x_22_);
if (v___x_24_ == 0)
{
lean_dec_ref(v___x_21_);
return v_init_19_;
}
else
{
size_t v___x_25_; size_t v___x_26_; lean_object* v___x_27_; 
v___x_25_ = lean_usize_of_nat(v___x_22_);
v___x_26_ = ((size_t)0ULL);
v___x_27_ = lp_FiniteQuantum___private_Init_Data_Array_Basic_0__Array_foldrMUnsafe_fold___at___00List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0_spec__0(v___x_21_, v___x_25_, v___x_26_, v_init_19_);
lean_dec_ref(v___x_21_);
return v___x_27_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_SymbolGame_expressivityNorm(lean_object* v_h_28_){
_start:
{
lean_object* v___x_29_; lean_object* v___x_30_; 
v___x_29_ = lean_unsigned_to_nat(0u);
v___x_30_ = lp_FiniteQuantum_List_foldrTR___at___00OmegaCosmology_SymbolGame_expressivityNorm_spec__0(v___x_29_, v_h_28_);
return v___x_30_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_Expressivity(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
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
