// Lean compiler output
// Module: WorldReconstructionRetraction
// Imports: public import Init public meta import Init public import WorldFiniteReconstruction
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
lean_object* lp_FiniteQuantum_OmegaWorld_probabilityCount(uint8_t, uint8_t);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixAdd(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixAdd___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixScale(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixScale___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMul(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMul___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_trace2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState(uint8_t, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMatches(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMatches___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*1, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState___boxed, .m_arity = 3, .m_num_fixed = 1, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1))} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*1, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState___boxed, .m_arity = 3, .m_num_fixed = 1, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1))} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__1 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*1, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState___boxed, .m_arity = 3, .m_num_fixed = 1, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1))} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__2 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__3 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__3_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__4 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__5 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_effectProjector(uint8_t, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_effectProjector___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_bornCount(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_bornCount___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_packageConditional___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_packageConditional(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_exposeConditional___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_exposeConditional(lean_object*, lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState___boxed, .m_arity = 3, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__1 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_effectProjector___boxed, .m_arity = 3, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__2 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*5 + 16, .m_other = 5, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(25) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__0_value),((lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__1_value),((lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__2_value),((lean_object*)(((size_t)(0) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__3 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__3_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_diagonalReconstructionRetraction___closed__3_value;
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(0u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix(uint8_t v___row_3_, uint8_t v___column_4_){
_start:
{
lean_object* v___x_5_; 
v___x_5_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0);
return v___x_5_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___boxed(lean_object* v___row_6_, lean_object* v___column_7_){
_start:
{
uint8_t v___row_boxed_8_; uint8_t v___column_boxed_9_; lean_object* v_res_10_; 
v___row_boxed_8_ = lean_unbox(v___row_6_);
v___column_boxed_9_ = lean_unbox(v___column_7_);
v_res_10_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix(v___row_boxed_8_, v___column_boxed_9_);
return v_res_10_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; 
v___x_11_ = lean_unsigned_to_nat(1u);
v___x_12_ = lean_nat_to_int(v___x_11_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix(uint8_t v_x_13_, uint8_t v_x_14_){
_start:
{
if (v_x_13_ == 0)
{
if (v_x_14_ == 0)
{
goto v___jp_15_;
}
else
{
goto v___jp_17_;
}
}
else
{
if (v_x_14_ == 1)
{
goto v___jp_15_;
}
else
{
goto v___jp_17_;
}
}
v___jp_15_:
{
lean_object* v___x_16_; 
v___x_16_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0);
return v___x_16_;
}
v___jp_17_:
{
lean_object* v___x_18_; 
v___x_18_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0);
return v___x_18_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___boxed(lean_object* v_x_19_, lean_object* v_x_20_){
_start:
{
uint8_t v_x_52__boxed_21_; uint8_t v_x_53__boxed_22_; lean_object* v_res_23_; 
v_x_52__boxed_21_ = lean_unbox(v_x_19_);
v_x_53__boxed_22_ = lean_unbox(v_x_20_);
v_res_23_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix(v_x_52__boxed_21_, v_x_53__boxed_22_);
return v_res_23_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixAdd(lean_object* v_left_24_, lean_object* v_right_25_, uint8_t v_row_26_, uint8_t v_column_27_){
_start:
{
lean_object* v___x_28_; lean_object* v___x_29_; lean_object* v___x_30_; lean_object* v___x_31_; lean_object* v___x_32_; lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_28_ = lean_box(v_row_26_);
v___x_29_ = lean_box(v_column_27_);
v___x_30_ = lean_apply_2(v_left_24_, v___x_28_, v___x_29_);
v___x_31_ = lean_box(v_row_26_);
v___x_32_ = lean_box(v_column_27_);
v___x_33_ = lean_apply_2(v_right_25_, v___x_31_, v___x_32_);
v___x_34_ = lean_int_add(v___x_30_, v___x_33_);
lean_dec(v___x_33_);
lean_dec(v___x_30_);
return v___x_34_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixAdd___boxed(lean_object* v_left_35_, lean_object* v_right_36_, lean_object* v_row_37_, lean_object* v_column_38_){
_start:
{
uint8_t v_row_boxed_39_; uint8_t v_column_boxed_40_; lean_object* v_res_41_; 
v_row_boxed_39_ = lean_unbox(v_row_37_);
v_column_boxed_40_ = lean_unbox(v_column_38_);
v_res_41_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixAdd(v_left_35_, v_right_36_, v_row_boxed_39_, v_column_boxed_40_);
return v_res_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixScale(lean_object* v_scalar_42_, lean_object* v_matrix_43_, uint8_t v_row_44_, uint8_t v_column_45_){
_start:
{
lean_object* v___x_46_; lean_object* v___x_47_; lean_object* v___x_48_; lean_object* v___x_49_; 
v___x_46_ = lean_box(v_row_44_);
v___x_47_ = lean_box(v_column_45_);
v___x_48_ = lean_apply_2(v_matrix_43_, v___x_46_, v___x_47_);
v___x_49_ = lean_int_mul(v_scalar_42_, v___x_48_);
lean_dec(v___x_48_);
return v___x_49_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixScale___boxed(lean_object* v_scalar_50_, lean_object* v_matrix_51_, lean_object* v_row_52_, lean_object* v_column_53_){
_start:
{
uint8_t v_row_boxed_54_; uint8_t v_column_boxed_55_; lean_object* v_res_56_; 
v_row_boxed_54_ = lean_unbox(v_row_52_);
v_column_boxed_55_ = lean_unbox(v_column_53_);
v_res_56_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixScale(v_scalar_50_, v_matrix_51_, v_row_boxed_54_, v_column_boxed_55_);
lean_dec(v_scalar_50_);
return v_res_56_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMul(lean_object* v_left_57_, lean_object* v_right_58_, uint8_t v_row_59_, uint8_t v_column_60_){
_start:
{
uint8_t v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; uint8_t v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; lean_object* v___x_74_; lean_object* v___x_75_; lean_object* v___x_76_; lean_object* v___x_77_; 
v___x_61_ = 0;
v___x_62_ = lean_box(v_row_59_);
v___x_63_ = lean_box(v___x_61_);
lean_inc_ref(v_left_57_);
v___x_64_ = lean_apply_2(v_left_57_, v___x_62_, v___x_63_);
v___x_65_ = lean_box(v___x_61_);
v___x_66_ = lean_box(v_column_60_);
lean_inc_ref(v_right_58_);
v___x_67_ = lean_apply_2(v_right_58_, v___x_65_, v___x_66_);
v___x_68_ = lean_int_mul(v___x_64_, v___x_67_);
lean_dec(v___x_67_);
lean_dec(v___x_64_);
v___x_69_ = 1;
v___x_70_ = lean_box(v_row_59_);
v___x_71_ = lean_box(v___x_69_);
v___x_72_ = lean_apply_2(v_left_57_, v___x_70_, v___x_71_);
v___x_73_ = lean_box(v___x_69_);
v___x_74_ = lean_box(v_column_60_);
v___x_75_ = lean_apply_2(v_right_58_, v___x_73_, v___x_74_);
v___x_76_ = lean_int_mul(v___x_72_, v___x_75_);
lean_dec(v___x_75_);
lean_dec(v___x_72_);
v___x_77_ = lean_int_add(v___x_68_, v___x_76_);
lean_dec(v___x_76_);
lean_dec(v___x_68_);
return v___x_77_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMul___boxed(lean_object* v_left_78_, lean_object* v_right_79_, lean_object* v_row_80_, lean_object* v_column_81_){
_start:
{
uint8_t v_row_boxed_82_; uint8_t v_column_boxed_83_; lean_object* v_res_84_; 
v_row_boxed_82_ = lean_unbox(v_row_80_);
v_column_boxed_83_ = lean_unbox(v_column_81_);
v_res_84_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMul(v_left_78_, v_right_79_, v_row_boxed_82_, v_column_boxed_83_);
return v_res_84_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_trace2(lean_object* v_matrix_85_){
_start:
{
uint8_t v___x_86_; lean_object* v___x_87_; lean_object* v___x_88_; lean_object* v___x_89_; uint8_t v___x_90_; lean_object* v___x_91_; lean_object* v___x_92_; lean_object* v___x_93_; lean_object* v___x_94_; 
v___x_86_ = 0;
v___x_87_ = lean_box(v___x_86_);
v___x_88_ = lean_box(v___x_86_);
lean_inc_ref(v_matrix_85_);
v___x_89_ = lean_apply_2(v_matrix_85_, v___x_87_, v___x_88_);
v___x_90_ = 1;
v___x_91_ = lean_box(v___x_90_);
v___x_92_ = lean_box(v___x_90_);
v___x_93_ = lean_apply_2(v_matrix_85_, v___x_91_, v___x_92_);
v___x_94_ = lean_int_add(v___x_89_, v___x_93_);
lean_dec(v___x_93_);
lean_dec(v___x_89_);
return v___x_94_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState(uint8_t v_state_95_, uint8_t v_x_96_, uint8_t v_x_97_){
_start:
{
if (v_x_96_ == 0)
{
if (v_x_97_ == 0)
{
lean_object* v___x_100_; lean_object* v___x_101_; 
v___x_100_ = lp_FiniteQuantum_OmegaWorld_probabilityCount(v_state_95_, v_x_97_);
v___x_101_ = lean_nat_to_int(v___x_100_);
return v___x_101_;
}
else
{
goto v___jp_98_;
}
}
else
{
if (v_x_97_ == 1)
{
lean_object* v___x_102_; lean_object* v___x_103_; 
v___x_102_ = lp_FiniteQuantum_OmegaWorld_probabilityCount(v_state_95_, v_x_97_);
v___x_103_ = lean_nat_to_int(v___x_102_);
return v___x_103_;
}
else
{
goto v___jp_98_;
}
}
v___jp_98_:
{
lean_object* v___x_99_; 
v___x_99_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0);
return v___x_99_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState___boxed(lean_object* v_state_104_, lean_object* v_x_105_, lean_object* v_x_106_){
_start:
{
uint8_t v_state_boxed_107_; uint8_t v_x_59__boxed_108_; uint8_t v_x_60__boxed_109_; lean_object* v_res_110_; 
v_state_boxed_107_ = lean_unbox(v_state_104_);
v_x_59__boxed_108_ = lean_unbox(v_x_105_);
v_x_60__boxed_109_ = lean_unbox(v_x_106_);
v_res_110_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState(v_state_boxed_107_, v_x_59__boxed_108_, v_x_60__boxed_109_);
return v_res_110_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMatches(lean_object* v_left_111_, lean_object* v_right_112_){
_start:
{
uint8_t v___y_114_; uint8_t v___x_131_; lean_object* v___x_132_; lean_object* v___x_133_; lean_object* v___x_134_; lean_object* v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; uint8_t v___x_138_; 
v___x_131_ = 0;
v___x_132_ = lean_box(v___x_131_);
v___x_133_ = lean_box(v___x_131_);
lean_inc_ref(v_left_111_);
v___x_134_ = lean_apply_2(v_left_111_, v___x_132_, v___x_133_);
v___x_135_ = lean_box(v___x_131_);
v___x_136_ = lean_box(v___x_131_);
lean_inc_ref(v_right_112_);
v___x_137_ = lean_apply_2(v_right_112_, v___x_135_, v___x_136_);
v___x_138_ = lean_int_dec_eq(v___x_134_, v___x_137_);
lean_dec(v___x_137_);
lean_dec(v___x_134_);
if (v___x_138_ == 0)
{
v___y_114_ = v___x_138_;
goto v___jp_113_;
}
else
{
uint8_t v___x_139_; lean_object* v___x_140_; lean_object* v___x_141_; lean_object* v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; lean_object* v___x_145_; uint8_t v___x_146_; 
v___x_139_ = 1;
v___x_140_ = lean_box(v___x_131_);
v___x_141_ = lean_box(v___x_139_);
lean_inc_ref(v_left_111_);
v___x_142_ = lean_apply_2(v_left_111_, v___x_140_, v___x_141_);
v___x_143_ = lean_box(v___x_131_);
v___x_144_ = lean_box(v___x_139_);
lean_inc_ref(v_right_112_);
v___x_145_ = lean_apply_2(v_right_112_, v___x_143_, v___x_144_);
v___x_146_ = lean_int_dec_eq(v___x_142_, v___x_145_);
lean_dec(v___x_145_);
lean_dec(v___x_142_);
v___y_114_ = v___x_146_;
goto v___jp_113_;
}
v___jp_113_:
{
if (v___y_114_ == 0)
{
lean_dec_ref(v_right_112_);
lean_dec_ref(v_left_111_);
return v___y_114_;
}
else
{
uint8_t v___x_115_; uint8_t v___x_116_; lean_object* v___x_117_; lean_object* v___x_118_; lean_object* v___x_119_; lean_object* v___x_120_; lean_object* v___x_121_; lean_object* v___x_122_; uint8_t v___x_123_; 
v___x_115_ = 1;
v___x_116_ = 0;
v___x_117_ = lean_box(v___x_115_);
v___x_118_ = lean_box(v___x_116_);
lean_inc_ref(v_left_111_);
v___x_119_ = lean_apply_2(v_left_111_, v___x_117_, v___x_118_);
v___x_120_ = lean_box(v___x_115_);
v___x_121_ = lean_box(v___x_116_);
lean_inc_ref(v_right_112_);
v___x_122_ = lean_apply_2(v_right_112_, v___x_120_, v___x_121_);
v___x_123_ = lean_int_dec_eq(v___x_119_, v___x_122_);
lean_dec(v___x_122_);
lean_dec(v___x_119_);
if (v___x_123_ == 0)
{
lean_dec_ref(v_right_112_);
lean_dec_ref(v_left_111_);
return v___x_123_;
}
else
{
lean_object* v___x_124_; lean_object* v___x_125_; lean_object* v___x_126_; lean_object* v___x_127_; lean_object* v___x_128_; lean_object* v___x_129_; uint8_t v___x_130_; 
v___x_124_ = lean_box(v___x_115_);
v___x_125_ = lean_box(v___x_115_);
v___x_126_ = lean_apply_2(v_left_111_, v___x_124_, v___x_125_);
v___x_127_ = lean_box(v___x_115_);
v___x_128_ = lean_box(v___x_115_);
v___x_129_ = lean_apply_2(v_right_112_, v___x_127_, v___x_128_);
v___x_130_ = lean_int_dec_eq(v___x_126_, v___x_129_);
lean_dec(v___x_129_);
lean_dec(v___x_126_);
return v___x_130_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMatches___boxed(lean_object* v_left_147_, lean_object* v_right_148_){
_start:
{
uint8_t v_res_149_; lean_object* v_r_150_; 
v_res_149_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMatches(v_left_147_, v_right_148_);
v_r_150_ = lean_box(v_res_149_);
return v_r_150_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState(lean_object* v_matrix_169_){
_start:
{
lean_object* v___x_170_; uint8_t v___x_171_; 
v___x_170_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__0));
lean_inc_ref(v_matrix_169_);
v___x_171_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMatches(v_matrix_169_, v___x_170_);
if (v___x_171_ == 0)
{
lean_object* v___x_172_; uint8_t v___x_173_; 
v___x_172_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__1));
lean_inc_ref(v_matrix_169_);
v___x_173_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMatches(v_matrix_169_, v___x_172_);
if (v___x_173_ == 0)
{
lean_object* v___x_174_; uint8_t v___x_175_; 
v___x_174_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__2));
v___x_175_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMatches(v_matrix_169_, v___x_174_);
if (v___x_175_ == 0)
{
lean_object* v___x_176_; 
v___x_176_ = lean_box(0);
return v___x_176_;
}
else
{
lean_object* v___x_177_; 
v___x_177_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__3));
return v___x_177_;
}
}
else
{
lean_object* v___x_178_; 
lean_dec_ref(v_matrix_169_);
v___x_178_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__4));
return v___x_178_;
}
}
else
{
lean_object* v___x_179_; 
lean_dec_ref(v_matrix_169_);
v___x_179_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_decodeState___closed__5));
return v___x_179_;
}
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix___closed__0(void){
_start:
{
lean_object* v___x_180_; lean_object* v___x_181_; 
v___x_180_ = lean_unsigned_to_nat(25u);
v___x_181_ = lean_nat_to_int(v___x_180_);
return v___x_181_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix(uint8_t v_x_182_, uint8_t v_x_183_){
_start:
{
if (v_x_182_ == 0)
{
if (v_x_183_ == 0)
{
lean_object* v___x_184_; 
v___x_184_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix___closed__0);
return v___x_184_;
}
else
{
lean_object* v___x_185_; 
v___x_185_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0);
return v___x_185_;
}
}
else
{
lean_object* v___x_186_; 
v___x_186_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0);
return v___x_186_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix___boxed(lean_object* v_x_187_, lean_object* v_x_188_){
_start:
{
uint8_t v_x_54__boxed_189_; uint8_t v_x_55__boxed_190_; lean_object* v_res_191_; 
v_x_54__boxed_189_ = lean_unbox(v_x_187_);
v_x_55__boxed_190_ = lean_unbox(v_x_188_);
v_res_191_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_malformedMatrix(v_x_54__boxed_189_, v_x_55__boxed_190_);
return v_res_191_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal___closed__0(void){
_start:
{
lean_object* v___x_192_; lean_object* v___x_193_; 
v___x_192_ = lean_unsigned_to_nat(24u);
v___x_193_ = lean_nat_to_int(v___x_192_);
return v___x_193_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal(uint8_t v_x_194_, uint8_t v_x_195_){
_start:
{
if (v_x_194_ == 0)
{
if (v_x_195_ == 0)
{
lean_object* v___x_198_; 
v___x_198_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0);
return v___x_198_;
}
else
{
goto v___jp_196_;
}
}
else
{
if (v_x_195_ == 1)
{
lean_object* v___x_199_; 
v___x_199_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal___closed__0);
return v___x_199_;
}
else
{
goto v___jp_196_;
}
}
v___jp_196_:
{
lean_object* v___x_197_; 
v___x_197_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0);
return v___x_197_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal___boxed(lean_object* v_x_200_, lean_object* v_x_201_){
_start:
{
uint8_t v_x_63__boxed_202_; uint8_t v_x_64__boxed_203_; lean_object* v_res_204_; 
v_x_63__boxed_202_ = lean_unbox(v_x_200_);
v_x_64__boxed_203_ = lean_unbox(v_x_201_);
v_res_204_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_outsideImageDiagonal(v_x_63__boxed_202_, v_x_64__boxed_203_);
return v_res_204_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter___redArg(uint8_t v_x_205_, uint8_t v_x_206_, lean_object* v_h__1_207_, lean_object* v_h__2_208_, lean_object* v_h__3_209_){
_start:
{
if (v_x_205_ == 0)
{
lean_dec(v_h__2_208_);
if (v_x_206_ == 0)
{
lean_object* v___x_210_; lean_object* v___x_211_; 
lean_dec(v_h__3_209_);
v___x_210_ = lean_box(0);
v___x_211_ = lean_apply_1(v_h__1_207_, v___x_210_);
return v___x_211_;
}
else
{
lean_object* v___x_212_; lean_object* v___x_213_; lean_object* v___x_214_; 
lean_dec(v_h__1_207_);
v___x_212_ = lean_box(v_x_205_);
v___x_213_ = lean_box(v_x_206_);
v___x_214_ = lean_apply_4(v_h__3_209_, v___x_212_, v___x_213_, lean_box(0), lean_box(0));
return v___x_214_;
}
}
else
{
lean_dec(v_h__1_207_);
if (v_x_206_ == 1)
{
lean_object* v___x_215_; lean_object* v___x_216_; 
lean_dec(v_h__3_209_);
v___x_215_ = lean_box(0);
v___x_216_ = lean_apply_1(v_h__2_208_, v___x_215_);
return v___x_216_;
}
else
{
lean_object* v___x_217_; lean_object* v___x_218_; lean_object* v___x_219_; 
lean_dec(v_h__2_208_);
v___x_217_ = lean_box(v_x_205_);
v___x_218_ = lean_box(v_x_206_);
v___x_219_ = lean_apply_4(v_h__3_209_, v___x_217_, v___x_218_, lean_box(0), lean_box(0));
return v___x_219_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter___redArg___boxed(lean_object* v_x_220_, lean_object* v_x_221_, lean_object* v_h__1_222_, lean_object* v_h__2_223_, lean_object* v_h__3_224_){
_start:
{
uint8_t v_x_36__boxed_225_; uint8_t v_x_37__boxed_226_; lean_object* v_res_227_; 
v_x_36__boxed_225_ = lean_unbox(v_x_220_);
v_x_37__boxed_226_ = lean_unbox(v_x_221_);
v_res_227_ = lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter___redArg(v_x_36__boxed_225_, v_x_37__boxed_226_, v_h__1_222_, v_h__2_223_, v_h__3_224_);
return v_res_227_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter(lean_object* v_motive_228_, uint8_t v_x_229_, uint8_t v_x_230_, lean_object* v_h__1_231_, lean_object* v_h__2_232_, lean_object* v_h__3_233_){
_start:
{
if (v_x_229_ == 0)
{
lean_dec(v_h__2_232_);
if (v_x_230_ == 0)
{
lean_object* v___x_234_; lean_object* v___x_235_; 
lean_dec(v_h__3_233_);
v___x_234_ = lean_box(0);
v___x_235_ = lean_apply_1(v_h__1_231_, v___x_234_);
return v___x_235_;
}
else
{
lean_object* v___x_236_; lean_object* v___x_237_; lean_object* v___x_238_; 
lean_dec(v_h__1_231_);
v___x_236_ = lean_box(v_x_229_);
v___x_237_ = lean_box(v_x_230_);
v___x_238_ = lean_apply_4(v_h__3_233_, v___x_236_, v___x_237_, lean_box(0), lean_box(0));
return v___x_238_;
}
}
else
{
lean_dec(v_h__1_231_);
if (v_x_230_ == 1)
{
lean_object* v___x_239_; lean_object* v___x_240_; 
lean_dec(v_h__3_233_);
v___x_239_ = lean_box(0);
v___x_240_ = lean_apply_1(v_h__2_232_, v___x_239_);
return v___x_240_;
}
else
{
lean_object* v___x_241_; lean_object* v___x_242_; lean_object* v___x_243_; 
lean_dec(v_h__2_232_);
v___x_241_ = lean_box(v_x_229_);
v___x_242_ = lean_box(v_x_230_);
v___x_243_ = lean_apply_4(v_h__3_233_, v___x_241_, v___x_242_, lean_box(0), lean_box(0));
return v___x_243_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter___boxed(lean_object* v_motive_244_, lean_object* v_x_245_, lean_object* v_x_246_, lean_object* v_h__1_247_, lean_object* v_h__2_248_, lean_object* v_h__3_249_){
_start:
{
uint8_t v_x_62__boxed_250_; uint8_t v_x_63__boxed_251_; lean_object* v_res_252_; 
v_x_62__boxed_250_ = lean_unbox(v_x_245_);
v_x_63__boxed_251_ = lean_unbox(v_x_246_);
v_res_252_ = lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_ReconstructionQ12_identityMatrix_match__1_splitter(v_motive_244_, v_x_62__boxed_250_, v_x_63__boxed_251_, v_h__1_247_, v_h__2_248_, v_h__3_249_);
return v_res_252_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter___redArg(uint8_t v_x_253_, uint8_t v_x_254_, lean_object* v_h__1_255_, lean_object* v_h__2_256_, lean_object* v_h__3_257_, lean_object* v_h__4_258_, lean_object* v_h__5_259_, lean_object* v_h__6_260_){
_start:
{
switch(v_x_253_)
{
case 0:
{
lean_dec(v_h__6_260_);
lean_dec(v_h__5_259_);
lean_dec(v_h__4_258_);
lean_dec(v_h__3_257_);
if (v_x_254_ == 0)
{
lean_object* v___x_261_; lean_object* v___x_262_; 
lean_dec(v_h__2_256_);
v___x_261_ = lean_box(0);
v___x_262_ = lean_apply_1(v_h__1_255_, v___x_261_);
return v___x_262_;
}
else
{
lean_object* v___x_263_; lean_object* v___x_264_; 
lean_dec(v_h__1_255_);
v___x_263_ = lean_box(0);
v___x_264_ = lean_apply_1(v_h__2_256_, v___x_263_);
return v___x_264_;
}
}
case 1:
{
lean_dec(v_h__6_260_);
lean_dec(v_h__5_259_);
lean_dec(v_h__2_256_);
lean_dec(v_h__1_255_);
if (v_x_254_ == 0)
{
lean_object* v___x_265_; lean_object* v___x_266_; 
lean_dec(v_h__4_258_);
v___x_265_ = lean_box(0);
v___x_266_ = lean_apply_1(v_h__3_257_, v___x_265_);
return v___x_266_;
}
else
{
lean_object* v___x_267_; lean_object* v___x_268_; 
lean_dec(v_h__3_257_);
v___x_267_ = lean_box(0);
v___x_268_ = lean_apply_1(v_h__4_258_, v___x_267_);
return v___x_268_;
}
}
default: 
{
lean_dec(v_h__4_258_);
lean_dec(v_h__3_257_);
lean_dec(v_h__2_256_);
lean_dec(v_h__1_255_);
if (v_x_254_ == 0)
{
lean_object* v___x_269_; lean_object* v___x_270_; 
lean_dec(v_h__6_260_);
v___x_269_ = lean_box(0);
v___x_270_ = lean_apply_1(v_h__5_259_, v___x_269_);
return v___x_270_;
}
else
{
lean_object* v___x_271_; lean_object* v___x_272_; 
lean_dec(v_h__5_259_);
v___x_271_ = lean_box(0);
v___x_272_ = lean_apply_1(v_h__6_260_, v___x_271_);
return v___x_272_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter___redArg___boxed(lean_object* v_x_273_, lean_object* v_x_274_, lean_object* v_h__1_275_, lean_object* v_h__2_276_, lean_object* v_h__3_277_, lean_object* v_h__4_278_, lean_object* v_h__5_279_, lean_object* v_h__6_280_){
_start:
{
uint8_t v_x_65__boxed_281_; uint8_t v_x_66__boxed_282_; lean_object* v_res_283_; 
v_x_65__boxed_281_ = lean_unbox(v_x_273_);
v_x_66__boxed_282_ = lean_unbox(v_x_274_);
v_res_283_ = lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter___redArg(v_x_65__boxed_281_, v_x_66__boxed_282_, v_h__1_275_, v_h__2_276_, v_h__3_277_, v_h__4_278_, v_h__5_279_, v_h__6_280_);
return v_res_283_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter(lean_object* v_motive_284_, uint8_t v_x_285_, uint8_t v_x_286_, lean_object* v_h__1_287_, lean_object* v_h__2_288_, lean_object* v_h__3_289_, lean_object* v_h__4_290_, lean_object* v_h__5_291_, lean_object* v_h__6_292_){
_start:
{
switch(v_x_285_)
{
case 0:
{
lean_dec(v_h__6_292_);
lean_dec(v_h__5_291_);
lean_dec(v_h__4_290_);
lean_dec(v_h__3_289_);
if (v_x_286_ == 0)
{
lean_object* v___x_293_; lean_object* v___x_294_; 
lean_dec(v_h__2_288_);
v___x_293_ = lean_box(0);
v___x_294_ = lean_apply_1(v_h__1_287_, v___x_293_);
return v___x_294_;
}
else
{
lean_object* v___x_295_; lean_object* v___x_296_; 
lean_dec(v_h__1_287_);
v___x_295_ = lean_box(0);
v___x_296_ = lean_apply_1(v_h__2_288_, v___x_295_);
return v___x_296_;
}
}
case 1:
{
lean_dec(v_h__6_292_);
lean_dec(v_h__5_291_);
lean_dec(v_h__2_288_);
lean_dec(v_h__1_287_);
if (v_x_286_ == 0)
{
lean_object* v___x_297_; lean_object* v___x_298_; 
lean_dec(v_h__4_290_);
v___x_297_ = lean_box(0);
v___x_298_ = lean_apply_1(v_h__3_289_, v___x_297_);
return v___x_298_;
}
else
{
lean_object* v___x_299_; lean_object* v___x_300_; 
lean_dec(v_h__3_289_);
v___x_299_ = lean_box(0);
v___x_300_ = lean_apply_1(v_h__4_290_, v___x_299_);
return v___x_300_;
}
}
default: 
{
lean_dec(v_h__4_290_);
lean_dec(v_h__3_289_);
lean_dec(v_h__2_288_);
lean_dec(v_h__1_287_);
if (v_x_286_ == 0)
{
lean_object* v___x_301_; lean_object* v___x_302_; 
lean_dec(v_h__6_292_);
v___x_301_ = lean_box(0);
v___x_302_ = lean_apply_1(v_h__5_291_, v___x_301_);
return v___x_302_;
}
else
{
lean_object* v___x_303_; lean_object* v___x_304_; 
lean_dec(v_h__5_291_);
v___x_303_ = lean_box(0);
v___x_304_ = lean_apply_1(v_h__6_292_, v___x_303_);
return v___x_304_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter___boxed(lean_object* v_motive_305_, lean_object* v_x_306_, lean_object* v_x_307_, lean_object* v_h__1_308_, lean_object* v_h__2_309_, lean_object* v_h__3_310_, lean_object* v_h__4_311_, lean_object* v_h__5_312_, lean_object* v_h__6_313_){
_start:
{
uint8_t v_x_95__boxed_314_; uint8_t v_x_96__boxed_315_; lean_object* v_res_316_; 
v_x_95__boxed_314_ = lean_unbox(v_x_306_);
v_x_96__boxed_315_ = lean_unbox(v_x_307_);
v_res_316_ = lp_FiniteQuantum___private_WorldReconstructionRetraction_0__OmegaWorld_probabilityCount_match__1_splitter(v_motive_305_, v_x_95__boxed_314_, v_x_96__boxed_315_, v_h__1_308_, v_h__2_309_, v_h__3_310_, v_h__4_311_, v_h__5_312_, v_h__6_313_);
return v_res_316_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_effectProjector(uint8_t v_x_317_, uint8_t v_x_318_, uint8_t v_x_319_){
_start:
{
if (v_x_317_ == 0)
{
if (v_x_318_ == 0)
{
if (v_x_319_ == 0)
{
goto v___jp_320_;
}
else
{
goto v___jp_322_;
}
}
else
{
goto v___jp_322_;
}
}
else
{
if (v_x_318_ == 1)
{
if (v_x_319_ == 1)
{
goto v___jp_320_;
}
else
{
goto v___jp_322_;
}
}
else
{
goto v___jp_322_;
}
}
v___jp_320_:
{
lean_object* v___x_321_; 
v___x_321_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_identityMatrix___closed__0);
return v___x_321_;
}
v___jp_322_:
{
lean_object* v___x_323_; 
v___x_323_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0, &lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_zeroMatrix___closed__0);
return v___x_323_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_effectProjector___boxed(lean_object* v_x_324_, lean_object* v_x_325_, lean_object* v_x_326_){
_start:
{
uint8_t v_x_68__boxed_327_; uint8_t v_x_69__boxed_328_; uint8_t v_x_70__boxed_329_; lean_object* v_res_330_; 
v_x_68__boxed_327_ = lean_unbox(v_x_324_);
v_x_69__boxed_328_ = lean_unbox(v_x_325_);
v_x_70__boxed_329_ = lean_unbox(v_x_326_);
v_res_330_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_effectProjector(v_x_68__boxed_327_, v_x_69__boxed_328_, v_x_70__boxed_329_);
return v_res_330_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_bornCount(uint8_t v_state_331_, uint8_t v_effect_332_){
_start:
{
lean_object* v___x_333_; lean_object* v___x_334_; lean_object* v___x_335_; lean_object* v___x_336_; lean_object* v___x_337_; lean_object* v___x_338_; 
v___x_333_ = lean_box(v_state_331_);
v___x_334_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_encodeState___boxed), 3, 1);
lean_closure_set(v___x_334_, 0, v___x_333_);
v___x_335_ = lean_box(v_effect_332_);
v___x_336_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_effectProjector___boxed), 3, 1);
lean_closure_set(v___x_336_, 0, v___x_335_);
v___x_337_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_matrixMul___boxed), 4, 2);
lean_closure_set(v___x_337_, 0, v___x_334_);
lean_closure_set(v___x_337_, 1, v___x_336_);
v___x_338_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_trace2(v___x_337_);
return v___x_338_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_bornCount___boxed(lean_object* v_state_339_, lean_object* v_effect_340_){
_start:
{
uint8_t v_state_boxed_341_; uint8_t v_effect_boxed_342_; lean_object* v_res_343_; 
v_state_boxed_341_ = lean_unbox(v_state_339_);
v_effect_boxed_342_ = lean_unbox(v_effect_340_);
v_res_343_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_bornCount(v_state_boxed_341_, v_effect_boxed_342_);
return v_res_343_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_packageConditional___redArg(lean_object* v_components_344_){
_start:
{
lean_object* v_fst_345_; lean_object* v_snd_346_; lean_object* v___x_348_; uint8_t v_isShared_349_; uint8_t v_isSharedCheck_353_; 
v_fst_345_ = lean_ctor_get(v_components_344_, 0);
v_snd_346_ = lean_ctor_get(v_components_344_, 1);
v_isSharedCheck_353_ = !lean_is_exclusive(v_components_344_);
if (v_isSharedCheck_353_ == 0)
{
v___x_348_ = v_components_344_;
v_isShared_349_ = v_isSharedCheck_353_;
goto v_resetjp_347_;
}
else
{
lean_inc(v_snd_346_);
lean_inc(v_fst_345_);
lean_dec(v_components_344_);
v___x_348_ = lean_box(0);
v_isShared_349_ = v_isSharedCheck_353_;
goto v_resetjp_347_;
}
v_resetjp_347_:
{
lean_object* v___x_351_; 
if (v_isShared_349_ == 0)
{
v___x_351_ = v___x_348_;
goto v_reusejp_350_;
}
else
{
lean_object* v_reuseFailAlloc_352_; 
v_reuseFailAlloc_352_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_352_, 0, v_fst_345_);
lean_ctor_set(v_reuseFailAlloc_352_, 1, v_snd_346_);
v___x_351_ = v_reuseFailAlloc_352_;
goto v_reusejp_350_;
}
v_reusejp_350_:
{
return v___x_351_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_packageConditional(lean_object* v_Imports_354_, lean_object* v_Recovery_355_, lean_object* v_components_356_){
_start:
{
lean_object* v___x_357_; 
v___x_357_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_packageConditional___redArg(v_components_356_);
return v___x_357_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_exposeConditional___redArg(lean_object* v_package_358_){
_start:
{
lean_object* v_explicitImports_359_; lean_object* v_conditionalRecovery_360_; lean_object* v___x_362_; uint8_t v_isShared_363_; uint8_t v_isSharedCheck_367_; 
v_explicitImports_359_ = lean_ctor_get(v_package_358_, 0);
v_conditionalRecovery_360_ = lean_ctor_get(v_package_358_, 1);
v_isSharedCheck_367_ = !lean_is_exclusive(v_package_358_);
if (v_isSharedCheck_367_ == 0)
{
v___x_362_ = v_package_358_;
v_isShared_363_ = v_isSharedCheck_367_;
goto v_resetjp_361_;
}
else
{
lean_inc(v_conditionalRecovery_360_);
lean_inc(v_explicitImports_359_);
lean_dec(v_package_358_);
v___x_362_ = lean_box(0);
v_isShared_363_ = v_isSharedCheck_367_;
goto v_resetjp_361_;
}
v_resetjp_361_:
{
lean_object* v___x_365_; 
if (v_isShared_363_ == 0)
{
v___x_365_ = v___x_362_;
goto v_reusejp_364_;
}
else
{
lean_object* v_reuseFailAlloc_366_; 
v_reuseFailAlloc_366_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_366_, 0, v_explicitImports_359_);
lean_ctor_set(v_reuseFailAlloc_366_, 1, v_conditionalRecovery_360_);
v___x_365_ = v_reuseFailAlloc_366_;
goto v_reusejp_364_;
}
v_reusejp_364_:
{
return v___x_365_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_exposeConditional(lean_object* v_Imports_368_, lean_object* v_Recovery_369_, lean_object* v_package_370_){
_start:
{
lean_object* v___x_371_; 
v___x_371_ = lp_FiniteQuantum_OmegaWorld_ReconstructionQ12_exposeConditional___redArg(v_package_370_);
return v___x_371_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_WorldFiniteReconstruction(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_WorldReconstructionRetraction(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_WorldFiniteReconstruction(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
