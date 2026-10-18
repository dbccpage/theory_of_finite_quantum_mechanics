// Lean compiler output
// Module: H042ShorNineQubitCode
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
lean_object* l_List_reverse___redArg(lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* l_Int_mul___boxed(lean_object*, lean_object*);
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
lean_object* l___private_Init_Data_List_Impl_0__List_zipWithTR_go___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_emod(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H042_dot__list_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H042_dot__list_spec__0___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Int_mul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1;
static const lean_array_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__2_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_list__sum(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_list__sum___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__7;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__8;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__6;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__7;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__6;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__7;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__8;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__6;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__z;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__x;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__6;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__z;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s8"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s7"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__16_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s6"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__17_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__17_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__18 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__18_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s5"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__19 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__19_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__19_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__20 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__20_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s4"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__21 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__21_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__21_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__22 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__22_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__23_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s3"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__23 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__23_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__24_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__23_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__24 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__24_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__25_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__25 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__25_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__26_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__25_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__26 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__26_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__27_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s2"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__27 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__27_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__28_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__27_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__28 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__28_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_evalSyndrome(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H042_basis__vec_spec__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H042_basis__vec_spec__0___boxed(lean_object*, lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(8) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(7) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(6) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(5) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__3_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(4) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__3_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__7_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__7_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__8_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_x__err(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_x__err___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__err(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__err___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_y__err(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_y__err___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H042_dot__list_spec__0(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
if (lean_obj_tag(v_x_2_) == 0)
{
return v_x_1_;
}
else
{
lean_object* v_head_3_; lean_object* v_tail_4_; lean_object* v___x_5_; 
v_head_3_ = lean_ctor_get(v_x_2_, 0);
v_tail_4_ = lean_ctor_get(v_x_2_, 1);
v___x_5_ = lean_int_add(v_x_1_, v_head_3_);
lean_dec(v_x_1_);
v_x_1_ = v___x_5_;
v_x_2_ = v_tail_4_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H042_dot__list_spec__0___boxed(lean_object* v_x_7_, lean_object* v_x_8_){
_start:
{
lean_object* v_res_9_; 
v_res_9_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H042_dot__list_spec__0(v_x_7_, v_x_8_);
lean_dec(v_x_8_);
return v_res_9_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; 
v___x_11_ = lean_unsigned_to_nat(0u);
v___x_12_ = lean_nat_to_int(v___x_11_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list(lean_object* v_l1_15_, lean_object* v_l2_16_){
_start:
{
lean_object* v___f_17_; lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; 
v___f_17_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__0));
v___x_18_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_19_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__2));
v___x_20_ = l___private_Init_Data_List_Impl_0__List_zipWithTR_go___redArg(v___f_17_, v_l1_15_, v_l2_16_, v___x_19_);
v___x_21_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H042_dot__list_spec__0(v___x_18_, v___x_20_);
lean_dec(v___x_20_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_list__sum(lean_object* v_l_22_){
_start:
{
lean_object* v___x_23_; lean_object* v___x_24_; 
v___x_23_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_24_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H042_dot__list_spec__0(v___x_23_, v_l_22_);
return v___x_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_list__sum___boxed(lean_object* v_l_25_){
_start:
{
lean_object* v_res_26_; 
v_res_26_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_list__sum(v_l_25_);
lean_dec(v_l_25_);
return v_res_26_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__0(void){
_start:
{
lean_object* v___x_27_; lean_object* v___x_28_; 
v___x_27_ = lean_unsigned_to_nat(2u);
v___x_28_ = lean_nat_to_int(v___x_27_);
return v___x_28_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1(void){
_start:
{
lean_object* v___x_29_; lean_object* v___x_30_; 
v___x_29_ = lean_unsigned_to_nat(1u);
v___x_30_ = lean_nat_to_int(v___x_29_);
return v___x_30_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__2(void){
_start:
{
lean_object* v___x_31_; lean_object* v___x_32_; 
v___x_31_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_32_ = lean_int_neg(v___x_31_);
return v___x_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(lean_object* v_x1_33_, lean_object* v_z1_34_, lean_object* v_x2_35_, lean_object* v_z2_36_){
_start:
{
lean_object* v___x_37_; lean_object* v___x_38_; lean_object* v___x_39_; lean_object* v___x_40_; lean_object* v___x_41_; lean_object* v___x_42_; uint8_t v___x_43_; 
v___x_37_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list(v_x1_33_, v_z2_36_);
v___x_38_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list(v_z1_34_, v_x2_35_);
v___x_39_ = lean_int_add(v___x_37_, v___x_38_);
lean_dec(v___x_38_);
lean_dec(v___x_37_);
v___x_40_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__0);
v___x_41_ = lean_int_emod(v___x_39_, v___x_40_);
lean_dec(v___x_39_);
v___x_42_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_43_ = lean_int_dec_eq(v___x_41_, v___x_42_);
lean_dec(v___x_41_);
if (v___x_43_ == 0)
{
lean_object* v___x_44_; 
v___x_44_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__2);
return v___x_44_;
}
else
{
lean_object* v___x_45_; 
v___x_45_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
return v___x_45_;
}
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0(void){
_start:
{
lean_object* v___x_46_; lean_object* v___x_47_; lean_object* v___x_48_; 
v___x_46_ = lean_box(0);
v___x_47_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_48_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_48_, 0, v___x_47_);
lean_ctor_set(v___x_48_, 1, v___x_46_);
return v___x_48_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1(void){
_start:
{
lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_49_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0);
v___x_50_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_51_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_51_, 0, v___x_50_);
lean_ctor_set(v___x_51_, 1, v___x_49_);
return v___x_51_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2(void){
_start:
{
lean_object* v___x_52_; lean_object* v___x_53_; lean_object* v___x_54_; 
v___x_52_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1);
v___x_53_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_54_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_54_, 0, v___x_53_);
lean_ctor_set(v___x_54_, 1, v___x_52_);
return v___x_54_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3(void){
_start:
{
lean_object* v___x_55_; lean_object* v___x_56_; lean_object* v___x_57_; 
v___x_55_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2);
v___x_56_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_57_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_57_, 0, v___x_56_);
lean_ctor_set(v___x_57_, 1, v___x_55_);
return v___x_57_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__4(void){
_start:
{
lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; 
v___x_58_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3);
v___x_59_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_60_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_60_, 0, v___x_59_);
lean_ctor_set(v___x_60_, 1, v___x_58_);
return v___x_60_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5(void){
_start:
{
lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; 
v___x_61_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__4);
v___x_62_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_63_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_63_, 0, v___x_62_);
lean_ctor_set(v___x_63_, 1, v___x_61_);
return v___x_63_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6(void){
_start:
{
lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; 
v___x_64_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5);
v___x_65_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_66_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_66_, 0, v___x_65_);
lean_ctor_set(v___x_66_, 1, v___x_64_);
return v___x_66_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__7(void){
_start:
{
lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; 
v___x_67_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6);
v___x_68_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_69_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_69_, 0, v___x_68_);
lean_ctor_set(v___x_69_, 1, v___x_67_);
return v___x_69_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__8(void){
_start:
{
lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; 
v___x_70_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__7);
v___x_71_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_72_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_72_, 0, v___x_71_);
lean_ctor_set(v___x_72_, 1, v___x_70_);
return v___x_72_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero(void){
_start:
{
lean_object* v___x_73_; 
v___x_73_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__8);
return v___x_73_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__0(void){
_start:
{
lean_object* v___x_74_; lean_object* v___x_75_; lean_object* v___x_76_; 
v___x_74_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__6);
v___x_75_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_76_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_76_, 0, v___x_75_);
lean_ctor_set(v___x_76_, 1, v___x_74_);
return v___x_76_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__1(void){
_start:
{
lean_object* v___x_77_; lean_object* v___x_78_; lean_object* v___x_79_; 
v___x_77_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__0);
v___x_78_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_79_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_79_, 0, v___x_78_);
lean_ctor_set(v___x_79_, 1, v___x_77_);
return v___x_79_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z(void){
_start:
{
lean_object* v___x_80_; 
v___x_80_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z___closed__1);
return v___x_80_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__0(void){
_start:
{
lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; 
v___x_81_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__5);
v___x_82_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_83_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_83_, 0, v___x_82_);
lean_ctor_set(v___x_83_, 1, v___x_81_);
return v___x_83_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1(void){
_start:
{
lean_object* v___x_84_; lean_object* v___x_85_; lean_object* v___x_86_; 
v___x_84_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__0);
v___x_85_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_86_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_86_, 0, v___x_85_);
lean_ctor_set(v___x_86_, 1, v___x_84_);
return v___x_86_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__2(void){
_start:
{
lean_object* v___x_87_; lean_object* v___x_88_; lean_object* v___x_89_; 
v___x_87_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1);
v___x_88_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_89_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_89_, 0, v___x_88_);
lean_ctor_set(v___x_89_, 1, v___x_87_);
return v___x_89_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z(void){
_start:
{
lean_object* v___x_90_; 
v___x_90_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__2);
return v___x_90_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__0(void){
_start:
{
lean_object* v___x_91_; lean_object* v___x_92_; lean_object* v___x_93_; 
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__3);
v___x_92_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_93_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_93_, 0, v___x_92_);
lean_ctor_set(v___x_93_, 1, v___x_91_);
return v___x_93_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__1(void){
_start:
{
lean_object* v___x_94_; lean_object* v___x_95_; lean_object* v___x_96_; 
v___x_94_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__0);
v___x_95_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_96_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_96_, 0, v___x_95_);
lean_ctor_set(v___x_96_, 1, v___x_94_);
return v___x_96_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__2(void){
_start:
{
lean_object* v___x_97_; lean_object* v___x_98_; lean_object* v___x_99_; 
v___x_97_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__1);
v___x_98_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_99_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_99_, 0, v___x_98_);
lean_ctor_set(v___x_99_, 1, v___x_97_);
return v___x_99_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__3(void){
_start:
{
lean_object* v___x_100_; lean_object* v___x_101_; lean_object* v___x_102_; 
v___x_100_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__2);
v___x_101_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_102_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_102_, 0, v___x_101_);
lean_ctor_set(v___x_102_, 1, v___x_100_);
return v___x_102_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__4(void){
_start:
{
lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; 
v___x_103_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__3);
v___x_104_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_105_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_105_, 0, v___x_104_);
lean_ctor_set(v___x_105_, 1, v___x_103_);
return v___x_105_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z(void){
_start:
{
lean_object* v___x_106_; 
v___x_106_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z___closed__4);
return v___x_106_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__0(void){
_start:
{
lean_object* v___x_107_; lean_object* v___x_108_; lean_object* v___x_109_; 
v___x_107_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__2);
v___x_108_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_109_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_109_, 0, v___x_108_);
lean_ctor_set(v___x_109_, 1, v___x_107_);
return v___x_109_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1(void){
_start:
{
lean_object* v___x_110_; lean_object* v___x_111_; lean_object* v___x_112_; 
v___x_110_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__0);
v___x_111_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_112_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_112_, 0, v___x_111_);
lean_ctor_set(v___x_112_, 1, v___x_110_);
return v___x_112_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__2(void){
_start:
{
lean_object* v___x_113_; lean_object* v___x_114_; lean_object* v___x_115_; 
v___x_113_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1);
v___x_114_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_115_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_115_, 0, v___x_114_);
lean_ctor_set(v___x_115_, 1, v___x_113_);
return v___x_115_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__3(void){
_start:
{
lean_object* v___x_116_; lean_object* v___x_117_; lean_object* v___x_118_; 
v___x_116_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__2);
v___x_117_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_118_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_118_, 0, v___x_117_);
lean_ctor_set(v___x_118_, 1, v___x_116_);
return v___x_118_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__4(void){
_start:
{
lean_object* v___x_119_; lean_object* v___x_120_; lean_object* v___x_121_; 
v___x_119_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__3);
v___x_120_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_121_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_121_, 0, v___x_120_);
lean_ctor_set(v___x_121_, 1, v___x_119_);
return v___x_121_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__5(void){
_start:
{
lean_object* v___x_122_; lean_object* v___x_123_; lean_object* v___x_124_; 
v___x_122_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__4);
v___x_123_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_124_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_124_, 0, v___x_123_);
lean_ctor_set(v___x_124_, 1, v___x_122_);
return v___x_124_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z(void){
_start:
{
lean_object* v___x_125_; 
v___x_125_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__5);
return v___x_125_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__0(void){
_start:
{
lean_object* v___x_126_; lean_object* v___x_127_; lean_object* v___x_128_; 
v___x_126_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__0);
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_128_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_128_, 0, v___x_127_);
lean_ctor_set(v___x_128_, 1, v___x_126_);
return v___x_128_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__1(void){
_start:
{
lean_object* v___x_129_; lean_object* v___x_130_; lean_object* v___x_131_; 
v___x_129_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__0);
v___x_130_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_131_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_131_, 0, v___x_130_);
lean_ctor_set(v___x_131_, 1, v___x_129_);
return v___x_131_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__2(void){
_start:
{
lean_object* v___x_132_; lean_object* v___x_133_; lean_object* v___x_134_; 
v___x_132_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__1);
v___x_133_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_134_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_134_, 0, v___x_133_);
lean_ctor_set(v___x_134_, 1, v___x_132_);
return v___x_134_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__3(void){
_start:
{
lean_object* v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; 
v___x_135_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__2);
v___x_136_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_137_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_137_, 0, v___x_136_);
lean_ctor_set(v___x_137_, 1, v___x_135_);
return v___x_137_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__4(void){
_start:
{
lean_object* v___x_138_; lean_object* v___x_139_; lean_object* v___x_140_; 
v___x_138_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__3);
v___x_139_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_140_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_140_, 0, v___x_139_);
lean_ctor_set(v___x_140_, 1, v___x_138_);
return v___x_140_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__5(void){
_start:
{
lean_object* v___x_141_; lean_object* v___x_142_; lean_object* v___x_143_; 
v___x_141_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__4);
v___x_142_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_143_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_143_, 0, v___x_142_);
lean_ctor_set(v___x_143_, 1, v___x_141_);
return v___x_143_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__6(void){
_start:
{
lean_object* v___x_144_; lean_object* v___x_145_; lean_object* v___x_146_; 
v___x_144_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__5);
v___x_145_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_146_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_146_, 0, v___x_145_);
lean_ctor_set(v___x_146_, 1, v___x_144_);
return v___x_146_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__7(void){
_start:
{
lean_object* v___x_147_; lean_object* v___x_148_; lean_object* v___x_149_; 
v___x_147_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__6);
v___x_148_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_149_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_149_, 0, v___x_148_);
lean_ctor_set(v___x_149_, 1, v___x_147_);
return v___x_149_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z(void){
_start:
{
lean_object* v___x_150_; 
v___x_150_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z___closed__7);
return v___x_150_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__0(void){
_start:
{
lean_object* v___x_151_; lean_object* v___x_152_; lean_object* v___x_153_; 
v___x_151_ = lean_box(0);
v___x_152_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_153_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_153_, 0, v___x_152_);
lean_ctor_set(v___x_153_, 1, v___x_151_);
return v___x_153_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1(void){
_start:
{
lean_object* v___x_154_; lean_object* v___x_155_; lean_object* v___x_156_; 
v___x_154_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__0);
v___x_155_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_156_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_156_, 0, v___x_155_);
lean_ctor_set(v___x_156_, 1, v___x_154_);
return v___x_156_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__2(void){
_start:
{
lean_object* v___x_157_; lean_object* v___x_158_; lean_object* v___x_159_; 
v___x_157_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1);
v___x_158_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_159_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_159_, 0, v___x_158_);
lean_ctor_set(v___x_159_, 1, v___x_157_);
return v___x_159_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__3(void){
_start:
{
lean_object* v___x_160_; lean_object* v___x_161_; lean_object* v___x_162_; 
v___x_160_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__2);
v___x_161_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_162_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_162_, 0, v___x_161_);
lean_ctor_set(v___x_162_, 1, v___x_160_);
return v___x_162_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__4(void){
_start:
{
lean_object* v___x_163_; lean_object* v___x_164_; lean_object* v___x_165_; 
v___x_163_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__3);
v___x_164_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_165_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_165_, 0, v___x_164_);
lean_ctor_set(v___x_165_, 1, v___x_163_);
return v___x_165_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__5(void){
_start:
{
lean_object* v___x_166_; lean_object* v___x_167_; lean_object* v___x_168_; 
v___x_166_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__4);
v___x_167_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_168_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_168_, 0, v___x_167_);
lean_ctor_set(v___x_168_, 1, v___x_166_);
return v___x_168_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__6(void){
_start:
{
lean_object* v___x_169_; lean_object* v___x_170_; lean_object* v___x_171_; 
v___x_169_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__5);
v___x_170_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_171_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_171_, 0, v___x_170_);
lean_ctor_set(v___x_171_, 1, v___x_169_);
return v___x_171_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__7(void){
_start:
{
lean_object* v___x_172_; lean_object* v___x_173_; lean_object* v___x_174_; 
v___x_172_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__6);
v___x_173_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_174_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_174_, 0, v___x_173_);
lean_ctor_set(v___x_174_, 1, v___x_172_);
return v___x_174_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__8(void){
_start:
{
lean_object* v___x_175_; lean_object* v___x_176_; lean_object* v___x_177_; 
v___x_175_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__7);
v___x_176_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_177_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_177_, 0, v___x_176_);
lean_ctor_set(v___x_177_, 1, v___x_175_);
return v___x_177_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z(void){
_start:
{
lean_object* v___x_178_; 
v___x_178_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__8);
return v___x_178_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__0(void){
_start:
{
lean_object* v___x_179_; lean_object* v___x_180_; lean_object* v___x_181_; 
v___x_179_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z___closed__1);
v___x_180_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_181_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_181_, 0, v___x_180_);
lean_ctor_set(v___x_181_, 1, v___x_179_);
return v___x_181_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__1(void){
_start:
{
lean_object* v___x_182_; lean_object* v___x_183_; lean_object* v___x_184_; 
v___x_182_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__0);
v___x_183_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_184_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_184_, 0, v___x_183_);
lean_ctor_set(v___x_184_, 1, v___x_182_);
return v___x_184_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__2(void){
_start:
{
lean_object* v___x_185_; lean_object* v___x_186_; lean_object* v___x_187_; 
v___x_185_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__1);
v___x_186_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_187_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_187_, 0, v___x_186_);
lean_ctor_set(v___x_187_, 1, v___x_185_);
return v___x_187_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__3(void){
_start:
{
lean_object* v___x_188_; lean_object* v___x_189_; lean_object* v___x_190_; 
v___x_188_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__2);
v___x_189_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_190_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_190_, 0, v___x_189_);
lean_ctor_set(v___x_190_, 1, v___x_188_);
return v___x_190_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x(void){
_start:
{
lean_object* v___x_191_; 
v___x_191_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x___closed__3);
return v___x_191_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__0(void){
_start:
{
lean_object* v___x_192_; lean_object* v___x_193_; lean_object* v___x_194_; 
v___x_192_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z___closed__1);
v___x_193_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_194_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_194_, 0, v___x_193_);
lean_ctor_set(v___x_194_, 1, v___x_192_);
return v___x_194_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__1(void){
_start:
{
lean_object* v___x_195_; lean_object* v___x_196_; lean_object* v___x_197_; 
v___x_195_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__0);
v___x_196_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_197_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_197_, 0, v___x_196_);
lean_ctor_set(v___x_197_, 1, v___x_195_);
return v___x_197_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__2(void){
_start:
{
lean_object* v___x_198_; lean_object* v___x_199_; lean_object* v___x_200_; 
v___x_198_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__1);
v___x_199_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_200_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_200_, 0, v___x_199_);
lean_ctor_set(v___x_200_, 1, v___x_198_);
return v___x_200_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3(void){
_start:
{
lean_object* v___x_201_; lean_object* v___x_202_; lean_object* v___x_203_; 
v___x_201_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__2);
v___x_202_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_203_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_203_, 0, v___x_202_);
lean_ctor_set(v___x_203_, 1, v___x_201_);
return v___x_203_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__4(void){
_start:
{
lean_object* v___x_204_; lean_object* v___x_205_; lean_object* v___x_206_; 
v___x_204_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3);
v___x_205_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_206_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_206_, 0, v___x_205_);
lean_ctor_set(v___x_206_, 1, v___x_204_);
return v___x_206_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__5(void){
_start:
{
lean_object* v___x_207_; lean_object* v___x_208_; lean_object* v___x_209_; 
v___x_207_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__4);
v___x_208_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_209_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_209_, 0, v___x_208_);
lean_ctor_set(v___x_209_, 1, v___x_207_);
return v___x_209_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__6(void){
_start:
{
lean_object* v___x_210_; lean_object* v___x_211_; lean_object* v___x_212_; 
v___x_210_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__5);
v___x_211_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_212_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_212_, 0, v___x_211_);
lean_ctor_set(v___x_212_, 1, v___x_210_);
return v___x_212_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x(void){
_start:
{
lean_object* v___x_213_; 
v___x_213_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__6);
return v___x_213_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__0(void){
_start:
{
lean_object* v___x_214_; lean_object* v___x_215_; lean_object* v___x_216_; 
v___x_214_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x___closed__3);
v___x_215_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_216_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_216_, 0, v___x_215_);
lean_ctor_set(v___x_216_, 1, v___x_214_);
return v___x_216_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__1(void){
_start:
{
lean_object* v___x_217_; lean_object* v___x_218_; lean_object* v___x_219_; 
v___x_217_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__0);
v___x_218_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_219_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_219_, 0, v___x_218_);
lean_ctor_set(v___x_219_, 1, v___x_217_);
return v___x_219_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__2(void){
_start:
{
lean_object* v___x_220_; lean_object* v___x_221_; lean_object* v___x_222_; 
v___x_220_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__1);
v___x_221_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_222_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_222_, 0, v___x_221_);
lean_ctor_set(v___x_222_, 1, v___x_220_);
return v___x_222_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x(void){
_start:
{
lean_object* v___x_223_; 
v___x_223_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x___closed__2);
return v___x_223_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__z(void){
_start:
{
lean_object* v___x_224_; 
v___x_224_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero;
return v___x_224_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__x(void){
_start:
{
lean_object* v___x_225_; 
v___x_225_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero;
return v___x_225_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__0(void){
_start:
{
lean_object* v___x_226_; lean_object* v___x_227_; lean_object* v___x_228_; 
v___x_226_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero___closed__1);
v___x_227_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_228_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_228_, 0, v___x_227_);
lean_ctor_set(v___x_228_, 1, v___x_226_);
return v___x_228_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__1(void){
_start:
{
lean_object* v___x_229_; lean_object* v___x_230_; lean_object* v___x_231_; 
v___x_229_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__0);
v___x_230_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_231_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_231_, 0, v___x_230_);
lean_ctor_set(v___x_231_, 1, v___x_229_);
return v___x_231_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__2(void){
_start:
{
lean_object* v___x_232_; lean_object* v___x_233_; lean_object* v___x_234_; 
v___x_232_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__1);
v___x_233_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_234_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_234_, 0, v___x_233_);
lean_ctor_set(v___x_234_, 1, v___x_232_);
return v___x_234_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__3(void){
_start:
{
lean_object* v___x_235_; lean_object* v___x_236_; lean_object* v___x_237_; 
v___x_235_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__2);
v___x_236_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_237_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_237_, 0, v___x_236_);
lean_ctor_set(v___x_237_, 1, v___x_235_);
return v___x_237_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__4(void){
_start:
{
lean_object* v___x_238_; lean_object* v___x_239_; lean_object* v___x_240_; 
v___x_238_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__3);
v___x_239_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_240_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_240_, 0, v___x_239_);
lean_ctor_set(v___x_240_, 1, v___x_238_);
return v___x_240_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__5(void){
_start:
{
lean_object* v___x_241_; lean_object* v___x_242_; lean_object* v___x_243_; 
v___x_241_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__4);
v___x_242_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_243_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_243_, 0, v___x_242_);
lean_ctor_set(v___x_243_, 1, v___x_241_);
return v___x_243_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__6(void){
_start:
{
lean_object* v___x_244_; lean_object* v___x_245_; lean_object* v___x_246_; 
v___x_244_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__5);
v___x_245_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_246_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_246_, 0, v___x_245_);
lean_ctor_set(v___x_246_, 1, v___x_244_);
return v___x_246_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z(void){
_start:
{
lean_object* v___x_247_; 
v___x_247_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z___closed__6);
return v___x_247_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x___closed__0(void){
_start:
{
lean_object* v___x_248_; lean_object* v___x_249_; lean_object* v___x_250_; 
v___x_248_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z___closed__1);
v___x_249_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_250_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_250_, 0, v___x_249_);
lean_ctor_set(v___x_250_, 1, v___x_248_);
return v___x_250_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x(void){
_start:
{
lean_object* v___x_251_; 
v___x_251_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x___closed__0);
return v___x_251_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__z(void){
_start:
{
lean_object* v___x_252_; 
v___x_252_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero;
return v___x_252_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8_decEq(lean_object* v_x_253_, lean_object* v_x_254_){
_start:
{
lean_object* v_s1_255_; lean_object* v_s2_256_; lean_object* v_s3_257_; lean_object* v_s4_258_; lean_object* v_s5_259_; lean_object* v_s6_260_; lean_object* v_s7_261_; lean_object* v_s8_262_; lean_object* v_s1_263_; lean_object* v_s2_264_; lean_object* v_s3_265_; lean_object* v_s4_266_; lean_object* v_s5_267_; lean_object* v_s6_268_; lean_object* v_s7_269_; lean_object* v_s8_270_; uint8_t v___x_271_; 
v_s1_255_ = lean_ctor_get(v_x_253_, 0);
v_s2_256_ = lean_ctor_get(v_x_253_, 1);
v_s3_257_ = lean_ctor_get(v_x_253_, 2);
v_s4_258_ = lean_ctor_get(v_x_253_, 3);
v_s5_259_ = lean_ctor_get(v_x_253_, 4);
v_s6_260_ = lean_ctor_get(v_x_253_, 5);
v_s7_261_ = lean_ctor_get(v_x_253_, 6);
v_s8_262_ = lean_ctor_get(v_x_253_, 7);
v_s1_263_ = lean_ctor_get(v_x_254_, 0);
v_s2_264_ = lean_ctor_get(v_x_254_, 1);
v_s3_265_ = lean_ctor_get(v_x_254_, 2);
v_s4_266_ = lean_ctor_get(v_x_254_, 3);
v_s5_267_ = lean_ctor_get(v_x_254_, 4);
v_s6_268_ = lean_ctor_get(v_x_254_, 5);
v_s7_269_ = lean_ctor_get(v_x_254_, 6);
v_s8_270_ = lean_ctor_get(v_x_254_, 7);
v___x_271_ = lean_int_dec_eq(v_s1_255_, v_s1_263_);
if (v___x_271_ == 0)
{
return v___x_271_;
}
else
{
uint8_t v___x_272_; 
v___x_272_ = lean_int_dec_eq(v_s2_256_, v_s2_264_);
if (v___x_272_ == 0)
{
return v___x_272_;
}
else
{
uint8_t v___x_273_; 
v___x_273_ = lean_int_dec_eq(v_s3_257_, v_s3_265_);
if (v___x_273_ == 0)
{
return v___x_273_;
}
else
{
uint8_t v___x_274_; 
v___x_274_ = lean_int_dec_eq(v_s4_258_, v_s4_266_);
if (v___x_274_ == 0)
{
return v___x_274_;
}
else
{
uint8_t v___x_275_; 
v___x_275_ = lean_int_dec_eq(v_s5_259_, v_s5_267_);
if (v___x_275_ == 0)
{
return v___x_275_;
}
else
{
uint8_t v___x_276_; 
v___x_276_ = lean_int_dec_eq(v_s6_260_, v_s6_268_);
if (v___x_276_ == 0)
{
return v___x_276_;
}
else
{
uint8_t v___x_277_; 
v___x_277_ = lean_int_dec_eq(v_s7_261_, v_s7_269_);
if (v___x_277_ == 0)
{
return v___x_277_;
}
else
{
uint8_t v___x_278_; 
v___x_278_ = lean_int_dec_eq(v_s8_262_, v_s8_270_);
return v___x_278_;
}
}
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8_decEq___boxed(lean_object* v_x_279_, lean_object* v_x_280_){
_start:
{
uint8_t v_res_281_; lean_object* v_r_282_; 
v_res_281_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8_decEq(v_x_279_, v_x_280_);
lean_dec_ref(v_x_280_);
lean_dec_ref(v_x_279_);
v_r_282_ = lean_box(v_res_281_);
return v_r_282_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8(lean_object* v_x_283_, lean_object* v_x_284_){
_start:
{
uint8_t v___x_285_; 
v___x_285_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8_decEq(v_x_283_, v_x_284_);
return v___x_285_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8___boxed(lean_object* v_x_286_, lean_object* v_x_287_){
_start:
{
uint8_t v_res_288_; lean_object* v_r_289_; 
v_res_288_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_instDecidableEqSyndrome8(v_x_286_, v_x_287_);
lean_dec_ref(v_x_287_);
lean_dec_ref(v_x_286_);
v_r_289_ = lean_box(v_res_288_);
return v_r_289_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_303_; lean_object* v___x_304_; 
v___x_303_ = lean_unsigned_to_nat(6u);
v___x_304_ = lean_nat_to_int(v___x_303_);
return v___x_304_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_306_; lean_object* v___x_307_; 
v___x_306_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__0));
v___x_307_ = lean_string_length(v___x_306_);
return v___x_307_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_308_; lean_object* v___x_309_; 
v___x_308_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__9);
v___x_309_ = lean_nat_to_int(v___x_308_);
return v___x_309_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg(lean_object* v_x_338_){
_start:
{
lean_object* v_s1_339_; lean_object* v_s2_340_; lean_object* v_s3_341_; lean_object* v_s4_342_; lean_object* v_s5_343_; lean_object* v_s6_344_; lean_object* v_s7_345_; lean_object* v_s8_346_; lean_object* v___x_347_; lean_object* v___x_348_; lean_object* v___x_349_; uint8_t v___y_351_; lean_object* v___y_352_; lean_object* v___y_353_; uint8_t v___y_365_; lean_object* v___y_366_; lean_object* v___y_367_; lean_object* v___y_368_; lean_object* v___y_369_; lean_object* v___y_387_; uint8_t v___y_388_; lean_object* v___y_389_; lean_object* v___y_390_; lean_object* v___y_391_; uint8_t v___y_409_; lean_object* v___y_410_; lean_object* v___y_411_; lean_object* v___y_412_; lean_object* v___y_413_; lean_object* v___y_431_; uint8_t v___y_432_; lean_object* v___y_433_; lean_object* v___y_434_; lean_object* v___y_435_; uint8_t v___y_453_; lean_object* v___y_454_; lean_object* v___y_455_; lean_object* v___y_456_; lean_object* v___y_457_; uint8_t v___y_475_; lean_object* v___y_476_; lean_object* v___y_477_; lean_object* v___y_478_; lean_object* v___y_479_; lean_object* v___y_497_; lean_object* v___x_517_; lean_object* v___x_518_; uint8_t v___x_519_; 
v_s1_339_ = lean_ctor_get(v_x_338_, 0);
v_s2_340_ = lean_ctor_get(v_x_338_, 1);
v_s3_341_ = lean_ctor_get(v_x_338_, 2);
v_s4_342_ = lean_ctor_get(v_x_338_, 3);
v_s5_343_ = lean_ctor_get(v_x_338_, 4);
v_s6_344_ = lean_ctor_get(v_x_338_, 5);
v_s7_345_ = lean_ctor_get(v_x_338_, 6);
v_s8_346_ = lean_ctor_get(v_x_338_, 7);
v___x_347_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__5));
v___x_348_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__6));
v___x_349_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__7);
v___x_517_ = lean_unsigned_to_nat(0u);
v___x_518_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_519_ = lean_int_dec_lt(v_s1_339_, v___x_518_);
if (v___x_519_ == 0)
{
lean_object* v___x_520_; lean_object* v___x_521_; 
v___x_520_ = l_Int_repr(v_s1_339_);
v___x_521_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_521_, 0, v___x_520_);
v___y_497_ = v___x_521_;
goto v___jp_496_;
}
else
{
lean_object* v___x_522_; lean_object* v___x_523_; lean_object* v___x_524_; 
v___x_522_ = l_Int_repr(v_s1_339_);
v___x_523_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_523_, 0, v___x_522_);
v___x_524_ = l_Repr_addAppParen(v___x_523_, v___x_517_);
v___y_497_ = v___x_524_;
goto v___jp_496_;
}
v___jp_350_:
{
lean_object* v___x_354_; lean_object* v___x_355_; lean_object* v___x_356_; lean_object* v___x_357_; lean_object* v___x_358_; lean_object* v___x_359_; lean_object* v___x_360_; lean_object* v___x_361_; lean_object* v___x_362_; lean_object* v___x_363_; 
v___x_354_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_354_, 0, v___x_349_);
lean_ctor_set(v___x_354_, 1, v___y_353_);
v___x_355_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_355_, 0, v___x_354_);
lean_ctor_set_uint8(v___x_355_, sizeof(void*)*1, v___y_351_);
v___x_356_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_356_, 0, v___y_352_);
lean_ctor_set(v___x_356_, 1, v___x_355_);
v___x_357_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__10);
v___x_358_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__11));
v___x_359_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_359_, 0, v___x_358_);
lean_ctor_set(v___x_359_, 1, v___x_356_);
v___x_360_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__12));
v___x_361_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_361_, 0, v___x_359_);
lean_ctor_set(v___x_361_, 1, v___x_360_);
v___x_362_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_362_, 0, v___x_357_);
lean_ctor_set(v___x_362_, 1, v___x_361_);
v___x_363_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_363_, 0, v___x_362_);
lean_ctor_set_uint8(v___x_363_, sizeof(void*)*1, v___y_351_);
return v___x_363_;
}
v___jp_364_:
{
lean_object* v___x_370_; lean_object* v___x_371_; lean_object* v___x_372_; lean_object* v___x_373_; lean_object* v___x_374_; lean_object* v___x_375_; lean_object* v___x_376_; lean_object* v___x_377_; lean_object* v___x_378_; lean_object* v___x_379_; uint8_t v___x_380_; 
v___x_370_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_370_, 0, v___x_349_);
lean_ctor_set(v___x_370_, 1, v___y_369_);
v___x_371_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_371_, 0, v___x_370_);
lean_ctor_set_uint8(v___x_371_, sizeof(void*)*1, v___y_365_);
v___x_372_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_372_, 0, v___y_368_);
lean_ctor_set(v___x_372_, 1, v___x_371_);
lean_inc(v___y_366_);
v___x_373_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_373_, 0, v___x_372_);
lean_ctor_set(v___x_373_, 1, v___y_366_);
lean_inc(v___y_367_);
v___x_374_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_374_, 0, v___x_373_);
lean_ctor_set(v___x_374_, 1, v___y_367_);
v___x_375_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__14));
v___x_376_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_376_, 0, v___x_374_);
lean_ctor_set(v___x_376_, 1, v___x_375_);
v___x_377_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_377_, 0, v___x_376_);
lean_ctor_set(v___x_377_, 1, v___x_347_);
v___x_378_ = lean_unsigned_to_nat(0u);
v___x_379_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_380_ = lean_int_dec_lt(v_s8_346_, v___x_379_);
if (v___x_380_ == 0)
{
lean_object* v___x_381_; lean_object* v___x_382_; 
v___x_381_ = l_Int_repr(v_s8_346_);
v___x_382_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_382_, 0, v___x_381_);
v___y_351_ = v___y_365_;
v___y_352_ = v___x_377_;
v___y_353_ = v___x_382_;
goto v___jp_350_;
}
else
{
lean_object* v___x_383_; lean_object* v___x_384_; lean_object* v___x_385_; 
v___x_383_ = l_Int_repr(v_s8_346_);
v___x_384_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_384_, 0, v___x_383_);
v___x_385_ = l_Repr_addAppParen(v___x_384_, v___x_378_);
v___y_351_ = v___y_365_;
v___y_352_ = v___x_377_;
v___y_353_ = v___x_385_;
goto v___jp_350_;
}
}
v___jp_386_:
{
lean_object* v___x_392_; lean_object* v___x_393_; lean_object* v___x_394_; lean_object* v___x_395_; lean_object* v___x_396_; lean_object* v___x_397_; lean_object* v___x_398_; lean_object* v___x_399_; lean_object* v___x_400_; lean_object* v___x_401_; uint8_t v___x_402_; 
v___x_392_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_392_, 0, v___x_349_);
lean_ctor_set(v___x_392_, 1, v___y_391_);
v___x_393_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_393_, 0, v___x_392_);
lean_ctor_set_uint8(v___x_393_, sizeof(void*)*1, v___y_388_);
v___x_394_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_394_, 0, v___y_387_);
lean_ctor_set(v___x_394_, 1, v___x_393_);
lean_inc(v___y_389_);
v___x_395_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_395_, 0, v___x_394_);
lean_ctor_set(v___x_395_, 1, v___y_389_);
lean_inc(v___y_390_);
v___x_396_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_396_, 0, v___x_395_);
lean_ctor_set(v___x_396_, 1, v___y_390_);
v___x_397_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__16));
v___x_398_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_398_, 0, v___x_396_);
lean_ctor_set(v___x_398_, 1, v___x_397_);
v___x_399_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_399_, 0, v___x_398_);
lean_ctor_set(v___x_399_, 1, v___x_347_);
v___x_400_ = lean_unsigned_to_nat(0u);
v___x_401_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_402_ = lean_int_dec_lt(v_s7_345_, v___x_401_);
if (v___x_402_ == 0)
{
lean_object* v___x_403_; lean_object* v___x_404_; 
v___x_403_ = l_Int_repr(v_s7_345_);
v___x_404_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_404_, 0, v___x_403_);
v___y_365_ = v___y_388_;
v___y_366_ = v___y_389_;
v___y_367_ = v___y_390_;
v___y_368_ = v___x_399_;
v___y_369_ = v___x_404_;
goto v___jp_364_;
}
else
{
lean_object* v___x_405_; lean_object* v___x_406_; lean_object* v___x_407_; 
v___x_405_ = l_Int_repr(v_s7_345_);
v___x_406_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_406_, 0, v___x_405_);
v___x_407_ = l_Repr_addAppParen(v___x_406_, v___x_400_);
v___y_365_ = v___y_388_;
v___y_366_ = v___y_389_;
v___y_367_ = v___y_390_;
v___y_368_ = v___x_399_;
v___y_369_ = v___x_407_;
goto v___jp_364_;
}
}
v___jp_408_:
{
lean_object* v___x_414_; lean_object* v___x_415_; lean_object* v___x_416_; lean_object* v___x_417_; lean_object* v___x_418_; lean_object* v___x_419_; lean_object* v___x_420_; lean_object* v___x_421_; lean_object* v___x_422_; lean_object* v___x_423_; uint8_t v___x_424_; 
v___x_414_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_414_, 0, v___x_349_);
lean_ctor_set(v___x_414_, 1, v___y_413_);
v___x_415_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_415_, 0, v___x_414_);
lean_ctor_set_uint8(v___x_415_, sizeof(void*)*1, v___y_409_);
v___x_416_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_416_, 0, v___y_410_);
lean_ctor_set(v___x_416_, 1, v___x_415_);
lean_inc(v___y_411_);
v___x_417_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_417_, 0, v___x_416_);
lean_ctor_set(v___x_417_, 1, v___y_411_);
lean_inc(v___y_412_);
v___x_418_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_418_, 0, v___x_417_);
lean_ctor_set(v___x_418_, 1, v___y_412_);
v___x_419_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__18));
v___x_420_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_420_, 0, v___x_418_);
lean_ctor_set(v___x_420_, 1, v___x_419_);
v___x_421_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_421_, 0, v___x_420_);
lean_ctor_set(v___x_421_, 1, v___x_347_);
v___x_422_ = lean_unsigned_to_nat(0u);
v___x_423_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_424_ = lean_int_dec_lt(v_s6_344_, v___x_423_);
if (v___x_424_ == 0)
{
lean_object* v___x_425_; lean_object* v___x_426_; 
v___x_425_ = l_Int_repr(v_s6_344_);
v___x_426_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_426_, 0, v___x_425_);
v___y_387_ = v___x_421_;
v___y_388_ = v___y_409_;
v___y_389_ = v___y_411_;
v___y_390_ = v___y_412_;
v___y_391_ = v___x_426_;
goto v___jp_386_;
}
else
{
lean_object* v___x_427_; lean_object* v___x_428_; lean_object* v___x_429_; 
v___x_427_ = l_Int_repr(v_s6_344_);
v___x_428_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_428_, 0, v___x_427_);
v___x_429_ = l_Repr_addAppParen(v___x_428_, v___x_422_);
v___y_387_ = v___x_421_;
v___y_388_ = v___y_409_;
v___y_389_ = v___y_411_;
v___y_390_ = v___y_412_;
v___y_391_ = v___x_429_;
goto v___jp_386_;
}
}
v___jp_430_:
{
lean_object* v___x_436_; lean_object* v___x_437_; lean_object* v___x_438_; lean_object* v___x_439_; lean_object* v___x_440_; lean_object* v___x_441_; lean_object* v___x_442_; lean_object* v___x_443_; lean_object* v___x_444_; lean_object* v___x_445_; uint8_t v___x_446_; 
v___x_436_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_436_, 0, v___x_349_);
lean_ctor_set(v___x_436_, 1, v___y_435_);
v___x_437_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_437_, 0, v___x_436_);
lean_ctor_set_uint8(v___x_437_, sizeof(void*)*1, v___y_432_);
v___x_438_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_438_, 0, v___y_431_);
lean_ctor_set(v___x_438_, 1, v___x_437_);
lean_inc(v___y_433_);
v___x_439_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_439_, 0, v___x_438_);
lean_ctor_set(v___x_439_, 1, v___y_433_);
lean_inc(v___y_434_);
v___x_440_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_440_, 0, v___x_439_);
lean_ctor_set(v___x_440_, 1, v___y_434_);
v___x_441_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__20));
v___x_442_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_442_, 0, v___x_440_);
lean_ctor_set(v___x_442_, 1, v___x_441_);
v___x_443_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_443_, 0, v___x_442_);
lean_ctor_set(v___x_443_, 1, v___x_347_);
v___x_444_ = lean_unsigned_to_nat(0u);
v___x_445_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_446_ = lean_int_dec_lt(v_s5_343_, v___x_445_);
if (v___x_446_ == 0)
{
lean_object* v___x_447_; lean_object* v___x_448_; 
v___x_447_ = l_Int_repr(v_s5_343_);
v___x_448_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_448_, 0, v___x_447_);
v___y_409_ = v___y_432_;
v___y_410_ = v___x_443_;
v___y_411_ = v___y_433_;
v___y_412_ = v___y_434_;
v___y_413_ = v___x_448_;
goto v___jp_408_;
}
else
{
lean_object* v___x_449_; lean_object* v___x_450_; lean_object* v___x_451_; 
v___x_449_ = l_Int_repr(v_s5_343_);
v___x_450_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_450_, 0, v___x_449_);
v___x_451_ = l_Repr_addAppParen(v___x_450_, v___x_444_);
v___y_409_ = v___y_432_;
v___y_410_ = v___x_443_;
v___y_411_ = v___y_433_;
v___y_412_ = v___y_434_;
v___y_413_ = v___x_451_;
goto v___jp_408_;
}
}
v___jp_452_:
{
lean_object* v___x_458_; lean_object* v___x_459_; lean_object* v___x_460_; lean_object* v___x_461_; lean_object* v___x_462_; lean_object* v___x_463_; lean_object* v___x_464_; lean_object* v___x_465_; lean_object* v___x_466_; lean_object* v___x_467_; uint8_t v___x_468_; 
v___x_458_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_458_, 0, v___x_349_);
lean_ctor_set(v___x_458_, 1, v___y_457_);
v___x_459_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_459_, 0, v___x_458_);
lean_ctor_set_uint8(v___x_459_, sizeof(void*)*1, v___y_453_);
v___x_460_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_460_, 0, v___y_456_);
lean_ctor_set(v___x_460_, 1, v___x_459_);
lean_inc(v___y_454_);
v___x_461_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_461_, 0, v___x_460_);
lean_ctor_set(v___x_461_, 1, v___y_454_);
lean_inc(v___y_455_);
v___x_462_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_462_, 0, v___x_461_);
lean_ctor_set(v___x_462_, 1, v___y_455_);
v___x_463_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__22));
v___x_464_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_464_, 0, v___x_462_);
lean_ctor_set(v___x_464_, 1, v___x_463_);
v___x_465_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_465_, 0, v___x_464_);
lean_ctor_set(v___x_465_, 1, v___x_347_);
v___x_466_ = lean_unsigned_to_nat(0u);
v___x_467_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_468_ = lean_int_dec_lt(v_s4_342_, v___x_467_);
if (v___x_468_ == 0)
{
lean_object* v___x_469_; lean_object* v___x_470_; 
v___x_469_ = l_Int_repr(v_s4_342_);
v___x_470_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_470_, 0, v___x_469_);
v___y_431_ = v___x_465_;
v___y_432_ = v___y_453_;
v___y_433_ = v___y_454_;
v___y_434_ = v___y_455_;
v___y_435_ = v___x_470_;
goto v___jp_430_;
}
else
{
lean_object* v___x_471_; lean_object* v___x_472_; lean_object* v___x_473_; 
v___x_471_ = l_Int_repr(v_s4_342_);
v___x_472_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_472_, 0, v___x_471_);
v___x_473_ = l_Repr_addAppParen(v___x_472_, v___x_466_);
v___y_431_ = v___x_465_;
v___y_432_ = v___y_453_;
v___y_433_ = v___y_454_;
v___y_434_ = v___y_455_;
v___y_435_ = v___x_473_;
goto v___jp_430_;
}
}
v___jp_474_:
{
lean_object* v___x_480_; lean_object* v___x_481_; lean_object* v___x_482_; lean_object* v___x_483_; lean_object* v___x_484_; lean_object* v___x_485_; lean_object* v___x_486_; lean_object* v___x_487_; lean_object* v___x_488_; lean_object* v___x_489_; uint8_t v___x_490_; 
v___x_480_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_480_, 0, v___x_349_);
lean_ctor_set(v___x_480_, 1, v___y_479_);
v___x_481_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_481_, 0, v___x_480_);
lean_ctor_set_uint8(v___x_481_, sizeof(void*)*1, v___y_475_);
v___x_482_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_482_, 0, v___y_476_);
lean_ctor_set(v___x_482_, 1, v___x_481_);
lean_inc(v___y_477_);
v___x_483_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_483_, 0, v___x_482_);
lean_ctor_set(v___x_483_, 1, v___y_477_);
lean_inc(v___y_478_);
v___x_484_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_484_, 0, v___x_483_);
lean_ctor_set(v___x_484_, 1, v___y_478_);
v___x_485_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__24));
v___x_486_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_486_, 0, v___x_484_);
lean_ctor_set(v___x_486_, 1, v___x_485_);
v___x_487_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_487_, 0, v___x_486_);
lean_ctor_set(v___x_487_, 1, v___x_347_);
v___x_488_ = lean_unsigned_to_nat(0u);
v___x_489_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_490_ = lean_int_dec_lt(v_s3_341_, v___x_489_);
if (v___x_490_ == 0)
{
lean_object* v___x_491_; lean_object* v___x_492_; 
v___x_491_ = l_Int_repr(v_s3_341_);
v___x_492_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_492_, 0, v___x_491_);
v___y_453_ = v___y_475_;
v___y_454_ = v___y_477_;
v___y_455_ = v___y_478_;
v___y_456_ = v___x_487_;
v___y_457_ = v___x_492_;
goto v___jp_452_;
}
else
{
lean_object* v___x_493_; lean_object* v___x_494_; lean_object* v___x_495_; 
v___x_493_ = l_Int_repr(v_s3_341_);
v___x_494_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_494_, 0, v___x_493_);
v___x_495_ = l_Repr_addAppParen(v___x_494_, v___x_488_);
v___y_453_ = v___y_475_;
v___y_454_ = v___y_477_;
v___y_455_ = v___y_478_;
v___y_456_ = v___x_487_;
v___y_457_ = v___x_495_;
goto v___jp_452_;
}
}
v___jp_496_:
{
lean_object* v___x_498_; uint8_t v___x_499_; lean_object* v___x_500_; lean_object* v___x_501_; lean_object* v___x_502_; lean_object* v___x_503_; lean_object* v___x_504_; lean_object* v___x_505_; lean_object* v___x_506_; lean_object* v___x_507_; lean_object* v___x_508_; lean_object* v___x_509_; lean_object* v___x_510_; uint8_t v___x_511_; 
v___x_498_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_498_, 0, v___x_349_);
lean_ctor_set(v___x_498_, 1, v___y_497_);
v___x_499_ = 0;
v___x_500_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_500_, 0, v___x_498_);
lean_ctor_set_uint8(v___x_500_, sizeof(void*)*1, v___x_499_);
v___x_501_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_501_, 0, v___x_348_);
lean_ctor_set(v___x_501_, 1, v___x_500_);
v___x_502_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__26));
v___x_503_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_503_, 0, v___x_501_);
lean_ctor_set(v___x_503_, 1, v___x_502_);
v___x_504_ = lean_box(1);
v___x_505_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_505_, 0, v___x_503_);
lean_ctor_set(v___x_505_, 1, v___x_504_);
v___x_506_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___closed__28));
v___x_507_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_507_, 0, v___x_505_);
lean_ctor_set(v___x_507_, 1, v___x_506_);
v___x_508_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_508_, 0, v___x_507_);
lean_ctor_set(v___x_508_, 1, v___x_347_);
v___x_509_ = lean_unsigned_to_nat(0u);
v___x_510_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___x_511_ = lean_int_dec_lt(v_s2_340_, v___x_510_);
if (v___x_511_ == 0)
{
lean_object* v___x_512_; lean_object* v___x_513_; 
v___x_512_ = l_Int_repr(v_s2_340_);
v___x_513_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_513_, 0, v___x_512_);
v___y_475_ = v___x_499_;
v___y_476_ = v___x_508_;
v___y_477_ = v___x_502_;
v___y_478_ = v___x_504_;
v___y_479_ = v___x_513_;
goto v___jp_474_;
}
else
{
lean_object* v___x_514_; lean_object* v___x_515_; lean_object* v___x_516_; 
v___x_514_ = l_Int_repr(v_s2_340_);
v___x_515_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_515_, 0, v___x_514_);
v___x_516_ = l_Repr_addAppParen(v___x_515_, v___x_509_);
v___y_475_ = v___x_499_;
v___y_476_ = v___x_508_;
v___y_477_ = v___x_502_;
v___y_478_ = v___x_504_;
v___y_479_ = v___x_516_;
goto v___jp_474_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg___boxed(lean_object* v_x_525_){
_start:
{
lean_object* v_res_526_; 
v_res_526_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg(v_x_525_);
lean_dec_ref(v_x_525_);
return v_res_526_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr(lean_object* v_x_527_, lean_object* v_prec_528_){
_start:
{
lean_object* v___x_529_; 
v___x_529_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___redArg(v_x_527_);
return v___x_529_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr___boxed(lean_object* v_x_530_, lean_object* v_prec_531_){
_start:
{
lean_object* v_res_532_; 
v_res_532_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_instReprSyndrome8_repr(v_x_530_, v_prec_531_);
lean_dec(v_prec_531_);
lean_dec_ref(v_x_530_);
return v_res_532_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome___closed__0(void){
_start:
{
lean_object* v___x_535_; lean_object* v___x_536_; 
v___x_535_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___x_536_ = lean_alloc_ctor(0, 8, 0);
lean_ctor_set(v___x_536_, 0, v___x_535_);
lean_ctor_set(v___x_536_, 1, v___x_535_);
lean_ctor_set(v___x_536_, 2, v___x_535_);
lean_ctor_set(v___x_536_, 3, v___x_535_);
lean_ctor_set(v___x_536_, 4, v___x_535_);
lean_ctor_set(v___x_536_, 5, v___x_535_);
lean_ctor_set(v___x_536_, 6, v___x_535_);
lean_ctor_set(v___x_536_, 7, v___x_535_);
return v___x_536_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome(void){
_start:
{
lean_object* v___x_537_; 
v___x_537_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome___closed__0);
return v___x_537_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_evalSyndrome(lean_object* v_ex_538_, lean_object* v_ez_539_){
_start:
{
lean_object* v___x_540_; lean_object* v___x_541_; lean_object* v___x_542_; lean_object* v___x_543_; lean_object* v___x_544_; lean_object* v___x_545_; lean_object* v___x_546_; lean_object* v___x_547_; lean_object* v___x_548_; lean_object* v___x_549_; lean_object* v___x_550_; lean_object* v___x_551_; lean_object* v___x_552_; lean_object* v___x_553_; lean_object* v___x_554_; lean_object* v___x_555_; lean_object* v___x_556_; lean_object* v___x_557_; 
v___x_540_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero;
v___x_541_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z;
lean_inc_n(v_ez_539_, 7);
lean_inc_n(v_ex_538_, 7);
v___x_542_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(v_ex_538_, v_ez_539_, v___x_540_, v___x_541_);
v___x_543_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z;
v___x_544_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(v_ex_538_, v_ez_539_, v___x_540_, v___x_543_);
v___x_545_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z;
v___x_546_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(v_ex_538_, v_ez_539_, v___x_540_, v___x_545_);
v___x_547_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z;
v___x_548_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(v_ex_538_, v_ez_539_, v___x_540_, v___x_547_);
v___x_549_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z;
v___x_550_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(v_ex_538_, v_ez_539_, v___x_540_, v___x_549_);
v___x_551_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z;
v___x_552_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(v_ex_538_, v_ez_539_, v___x_540_, v___x_551_);
v___x_553_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x;
v___x_554_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(v_ex_538_, v_ez_539_, v___x_553_, v___x_540_);
v___x_555_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x;
v___x_556_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase(v_ex_538_, v_ez_539_, v___x_555_, v___x_540_);
v___x_557_ = lean_alloc_ctor(0, 8, 0);
lean_ctor_set(v___x_557_, 0, v___x_542_);
lean_ctor_set(v___x_557_, 1, v___x_544_);
lean_ctor_set(v___x_557_, 2, v___x_546_);
lean_ctor_set(v___x_557_, 3, v___x_548_);
lean_ctor_set(v___x_557_, 4, v___x_550_);
lean_ctor_set(v___x_557_, 5, v___x_552_);
lean_ctor_set(v___x_557_, 6, v___x_554_);
lean_ctor_set(v___x_557_, 7, v___x_556_);
return v___x_557_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H042_basis__vec_spec__0(lean_object* v_idx_558_, lean_object* v_a_559_, lean_object* v_a_560_){
_start:
{
if (lean_obj_tag(v_a_559_) == 0)
{
lean_object* v___x_561_; 
v___x_561_ = l_List_reverse___redArg(v_a_560_);
return v___x_561_;
}
else
{
lean_object* v_head_562_; lean_object* v_tail_563_; lean_object* v___x_565_; uint8_t v_isShared_566_; uint8_t v_isSharedCheck_576_; 
v_head_562_ = lean_ctor_get(v_a_559_, 0);
v_tail_563_ = lean_ctor_get(v_a_559_, 1);
v_isSharedCheck_576_ = !lean_is_exclusive(v_a_559_);
if (v_isSharedCheck_576_ == 0)
{
v___x_565_ = v_a_559_;
v_isShared_566_ = v_isSharedCheck_576_;
goto v_resetjp_564_;
}
else
{
lean_inc(v_tail_563_);
lean_inc(v_head_562_);
lean_dec(v_a_559_);
v___x_565_ = lean_box(0);
v_isShared_566_ = v_isSharedCheck_576_;
goto v_resetjp_564_;
}
v_resetjp_564_:
{
lean_object* v___y_568_; uint8_t v___x_573_; 
v___x_573_ = lean_nat_dec_eq(v_head_562_, v_idx_558_);
lean_dec(v_head_562_);
if (v___x_573_ == 0)
{
lean_object* v___x_574_; 
v___x_574_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_dot__list___closed__1);
v___y_568_ = v___x_574_;
goto v___jp_567_;
}
else
{
lean_object* v___x_575_; 
v___x_575_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_pauli__phase___closed__1);
v___y_568_ = v___x_575_;
goto v___jp_567_;
}
v___jp_567_:
{
lean_object* v___x_570_; 
lean_inc(v___y_568_);
if (v_isShared_566_ == 0)
{
lean_ctor_set(v___x_565_, 1, v_a_560_);
lean_ctor_set(v___x_565_, 0, v___y_568_);
v___x_570_ = v___x_565_;
goto v_reusejp_569_;
}
else
{
lean_object* v_reuseFailAlloc_572_; 
v_reuseFailAlloc_572_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_572_, 0, v___y_568_);
lean_ctor_set(v_reuseFailAlloc_572_, 1, v_a_560_);
v___x_570_ = v_reuseFailAlloc_572_;
goto v_reusejp_569_;
}
v_reusejp_569_:
{
v_a_559_ = v_tail_563_;
v_a_560_ = v___x_570_;
goto _start;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H042_basis__vec_spec__0___boxed(lean_object* v_idx_577_, lean_object* v_a_578_, lean_object* v_a_579_){
_start:
{
lean_object* v_res_580_; 
v_res_580_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H042_basis__vec_spec__0(v_idx_577_, v_a_578_, v_a_579_);
lean_dec(v_idx_577_);
return v_res_580_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec(lean_object* v_idx_608_){
_start:
{
lean_object* v___x_609_; lean_object* v___x_610_; lean_object* v___x_611_; 
v___x_609_ = lean_box(0);
v___x_610_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___closed__8));
v___x_611_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H042_basis__vec_spec__0(v_idx_608_, v___x_610_, v___x_609_);
return v___x_611_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec___boxed(lean_object* v_idx_612_){
_start:
{
lean_object* v_res_613_; 
v_res_613_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec(v_idx_612_);
lean_dec(v_idx_612_);
return v_res_613_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_x__err(lean_object* v_i_614_){
_start:
{
lean_object* v___x_615_; lean_object* v___x_616_; lean_object* v___x_617_; 
v___x_615_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec(v_i_614_);
v___x_616_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero;
v___x_617_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_evalSyndrome(v___x_615_, v___x_616_);
return v___x_617_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_x__err___boxed(lean_object* v_i_618_){
_start:
{
lean_object* v_res_619_; 
v_res_619_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_x__err(v_i_618_);
lean_dec(v_i_618_);
return v_res_619_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__err(lean_object* v_i_620_){
_start:
{
lean_object* v___x_621_; lean_object* v___x_622_; lean_object* v___x_623_; 
v___x_621_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero;
v___x_622_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec(v_i_620_);
v___x_623_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_evalSyndrome(v___x_621_, v___x_622_);
return v___x_623_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__err___boxed(lean_object* v_i_624_){
_start:
{
lean_object* v_res_625_; 
v_res_625_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__err(v_i_624_);
lean_dec(v_i_624_);
return v_res_625_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_y__err(lean_object* v_i_626_){
_start:
{
lean_object* v___x_627_; lean_object* v___x_628_; 
v___x_627_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_basis__vec(v_i_626_);
lean_inc(v___x_627_);
v___x_628_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_evalSyndrome(v___x_627_, v___x_627_);
return v___x_628_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H042_y__err___boxed(lean_object* v_i_629_){
_start:
{
lean_object* v_res_630_; 
v_res_630_ = lp_FiniteQuantum_FableHilbertWalk20260819_H042_y__err(v_i_629_);
lean_dec(v_i_629_);
return v_res_630_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H042ShorNineQubitCode(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_z__zero);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_s1__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_s2__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_s3__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_s4__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_s5__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_s6__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_s7__x);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_s8__x);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__x);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__x = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__x();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__x);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_zl__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__x);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_xl3__z);
lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H042_trivialSyndrome);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
