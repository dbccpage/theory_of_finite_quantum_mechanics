// Lean compiler output
// Module: WorldResidualGrowth
// Imports: public import Init public meta import Init public import WorldPresentation
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_normalSpeedZero;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_accelerationL1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_barAUpper;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_exactNormalSpeedAtThreeFifths;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_escapingLowerAtThreeFifths;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_escapingUpperAtThreeFifths;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_clearedNormalNumerator;
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_normalSpeedZero(void){
_start:
{
lean_object* v___x_1_; 
v___x_1_ = lean_unsigned_to_nat(1u);
return v___x_1_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_accelerationL1(void){
_start:
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(10u);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_barAUpper(void){
_start:
{
lean_object* v___x_3_; 
v___x_3_ = lean_unsigned_to_nat(5u);
return v___x_3_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_exactNormalSpeedAtThreeFifths(void){
_start:
{
lean_object* v___x_4_; 
v___x_4_ = lean_unsigned_to_nat(7u);
return v___x_4_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_escapingLowerAtThreeFifths(void){
_start:
{
lean_object* v___x_5_; 
v___x_5_ = lean_unsigned_to_nat(0u);
return v___x_5_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_escapingUpperAtThreeFifths(void){
_start:
{
lean_object* v___x_6_; 
v___x_6_ = lean_unsigned_to_nat(7u);
return v___x_6_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_clearedNormalNumerator(void){
_start:
{
lean_object* v___x_7_; 
v___x_7_ = lean_unsigned_to_nat(35u);
return v___x_7_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_WorldPresentation(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_WorldResidualGrowth(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_WorldPresentation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_OmegaWorld_normalSpeedZero = _init_lp_FiniteQuantum_OmegaWorld_normalSpeedZero();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_normalSpeedZero);
lp_FiniteQuantum_OmegaWorld_accelerationL1 = _init_lp_FiniteQuantum_OmegaWorld_accelerationL1();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_accelerationL1);
lp_FiniteQuantum_OmegaWorld_barAUpper = _init_lp_FiniteQuantum_OmegaWorld_barAUpper();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_barAUpper);
lp_FiniteQuantum_OmegaWorld_exactNormalSpeedAtThreeFifths = _init_lp_FiniteQuantum_OmegaWorld_exactNormalSpeedAtThreeFifths();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_exactNormalSpeedAtThreeFifths);
lp_FiniteQuantum_OmegaWorld_escapingLowerAtThreeFifths = _init_lp_FiniteQuantum_OmegaWorld_escapingLowerAtThreeFifths();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_escapingLowerAtThreeFifths);
lp_FiniteQuantum_OmegaWorld_escapingUpperAtThreeFifths = _init_lp_FiniteQuantum_OmegaWorld_escapingUpperAtThreeFifths();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_escapingUpperAtThreeFifths);
lp_FiniteQuantum_OmegaWorld_clearedNormalNumerator = _init_lp_FiniteQuantum_OmegaWorld_clearedNormalNumerator();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_clearedNormalNumerator);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
