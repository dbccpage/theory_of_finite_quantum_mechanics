// Lean compiler output
// Module: HWKernel
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
lean_object* l_Rat_mul___boxed(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_string_length(lean_object*);
lean_object* l_Int_add___boxed(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* l_Nat_cast___at___00Dyadic_toRat_spec__0(lean_object*);
lean_object* l_Rat_neg(lean_object*);
lean_object* l_Rat_add(lean_object*, lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
lean_object* l_Int_neg___boxed(lean_object*);
lean_object* l_Int_mul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_HWKernel_0__FableHilbertWalk20260819_HWKernel_rsum_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_HWKernel_0__FableHilbertWalk20260819_HWKernel_rsum_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___lam__0___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Int_add___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Int_mul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Int_neg___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__2_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__6;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___lam__0___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Rat_add, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Rat_mul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Rat_neg, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__2_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__6;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "re"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "im"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__16_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__2_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__0(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__1(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__1___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__2(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__2___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__0___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__1___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__2___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*6 + 0, .m_other = 6, .m_tag = 0}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__1_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__0_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__2_value),((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__3_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___closed__3_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool___closed__1_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__3_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__3_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__2_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__1_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__0_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__7_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBoolProd___closed__7_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(lean_object* v_P_1_, lean_object* v_x_2_){
_start:
{
if (lean_obj_tag(v_x_2_) == 0)
{
lean_object* v_zero_3_; 
v_zero_3_ = lean_ctor_get(v_P_1_, 3);
lean_inc(v_zero_3_);
lean_dec_ref(v_P_1_);
return v_zero_3_;
}
else
{
lean_object* v_head_4_; lean_object* v_tail_5_; lean_object* v_add_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v_head_4_ = lean_ctor_get(v_x_2_, 0);
lean_inc(v_head_4_);
v_tail_5_ = lean_ctor_get(v_x_2_, 1);
lean_inc(v_tail_5_);
lean_dec_ref_known(v_x_2_, 2);
v_add_6_ = lean_ctor_get(v_P_1_, 0);
lean_inc(v_add_6_);
v___x_7_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v_P_1_, v_tail_5_);
v___x_8_ = lean_apply_2(v_add_6_, v_head_4_, v___x_7_);
return v___x_8_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum(lean_object* v_K_9_, lean_object* v_P_10_, lean_object* v_x_11_){
_start:
{
lean_object* v___x_12_; 
v___x_12_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v_P_10_, v_x_11_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_HWKernel_0__FableHilbertWalk20260819_HWKernel_rsum_match__1_splitter___redArg(lean_object* v_x_13_, lean_object* v_h__1_14_, lean_object* v_h__2_15_){
_start:
{
if (lean_obj_tag(v_x_13_) == 0)
{
lean_object* v___x_16_; lean_object* v___x_17_; 
lean_dec(v_h__2_15_);
v___x_16_ = lean_box(0);
v___x_17_ = lean_apply_1(v_h__1_14_, v___x_16_);
return v___x_17_;
}
else
{
lean_object* v_head_18_; lean_object* v_tail_19_; lean_object* v___x_20_; 
lean_dec(v_h__1_14_);
v_head_18_ = lean_ctor_get(v_x_13_, 0);
lean_inc(v_head_18_);
v_tail_19_ = lean_ctor_get(v_x_13_, 1);
lean_inc(v_tail_19_);
lean_dec_ref_known(v_x_13_, 2);
v___x_20_ = lean_apply_2(v_h__2_15_, v_head_18_, v_tail_19_);
return v___x_20_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_HWKernel_0__FableHilbertWalk20260819_HWKernel_rsum_match__1_splitter(lean_object* v_K_21_, lean_object* v_motive_22_, lean_object* v_x_23_, lean_object* v_h__1_24_, lean_object* v_h__2_25_){
_start:
{
if (lean_obj_tag(v_x_23_) == 0)
{
lean_object* v___x_26_; lean_object* v___x_27_; 
lean_dec(v_h__2_25_);
v___x_26_ = lean_box(0);
v___x_27_ = lean_apply_1(v_h__1_24_, v___x_26_);
return v___x_27_;
}
else
{
lean_object* v_head_28_; lean_object* v_tail_29_; lean_object* v___x_30_; 
lean_dec(v_h__1_24_);
v_head_28_ = lean_ctor_get(v_x_23_, 0);
lean_inc(v_head_28_);
v_tail_29_ = lean_ctor_get(v_x_23_, 1);
lean_inc(v_tail_29_);
lean_dec_ref_known(v_x_23_, 2);
v___x_30_ = lean_apply_2(v_h__2_25_, v_head_28_, v_tail_29_);
return v___x_30_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___lam__0(lean_object* v___y_31_){
_start:
{
lean_inc(v___y_31_);
return v___y_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___lam__0___boxed(lean_object* v___y_32_){
_start:
{
lean_object* v_res_33_; 
v_res_33_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___lam__0(v___y_32_);
lean_dec(v___y_32_);
return v_res_33_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4(void){
_start:
{
lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_38_ = lean_unsigned_to_nat(0u);
v___x_39_ = lean_nat_to_int(v___x_38_);
return v___x_39_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5(void){
_start:
{
lean_object* v___x_40_; lean_object* v___x_41_; 
v___x_40_ = lean_unsigned_to_nat(1u);
v___x_41_ = lean_nat_to_int(v___x_40_);
return v___x_41_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__6(void){
_start:
{
lean_object* v___f_42_; lean_object* v___x_43_; lean_object* v___x_44_; lean_object* v___f_45_; lean_object* v___f_46_; lean_object* v___f_47_; lean_object* v___x_48_; 
v___f_42_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__3));
v___x_43_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5);
v___x_44_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4);
v___f_45_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__2));
v___f_46_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__1));
v___f_47_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__0));
v___x_48_ = lean_alloc_ctor(0, 6, 0);
lean_ctor_set(v___x_48_, 0, v___f_47_);
lean_ctor_set(v___x_48_, 1, v___f_46_);
lean_ctor_set(v___x_48_, 2, v___f_45_);
lean_ctor_set(v___x_48_, 3, v___x_44_);
lean_ctor_set(v___x_48_, 4, v___x_43_);
lean_ctor_set(v___x_48_, 5, v___f_42_);
return v___x_48_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack(void){
_start:
{
lean_object* v___x_49_; 
v___x_49_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__6);
return v___x_49_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___lam__0(lean_object* v___y_50_){
_start:
{
lean_inc_ref(v___y_50_);
return v___y_50_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___lam__0___boxed(lean_object* v___y_51_){
_start:
{
lean_object* v_res_52_; 
v_res_52_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___lam__0(v___y_51_);
lean_dec_ref(v___y_51_);
return v_res_52_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__4(void){
_start:
{
lean_object* v___x_57_; lean_object* v___x_58_; 
v___x_57_ = lean_unsigned_to_nat(0u);
v___x_58_ = l_Nat_cast___at___00Dyadic_toRat_spec__0(v___x_57_);
return v___x_58_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__5(void){
_start:
{
lean_object* v___x_59_; lean_object* v___x_60_; 
v___x_59_ = lean_unsigned_to_nat(1u);
v___x_60_ = l_Nat_cast___at___00Dyadic_toRat_spec__0(v___x_59_);
return v___x_60_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__6(void){
_start:
{
lean_object* v___f_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___f_64_; lean_object* v___f_65_; lean_object* v___f_66_; lean_object* v___x_67_; 
v___f_61_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__3));
v___x_62_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__5);
v___x_63_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__4);
v___f_64_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__2));
v___f_65_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__1));
v___f_66_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__0));
v___x_67_ = lean_alloc_ctor(0, 6, 0);
lean_ctor_set(v___x_67_, 0, v___f_66_);
lean_ctor_set(v___x_67_, 1, v___f_65_);
lean_ctor_set(v___x_67_, 2, v___f_64_);
lean_ctor_set(v___x_67_, 3, v___x_63_);
lean_ctor_set(v___x_67_, 4, v___x_62_);
lean_ctor_set(v___x_67_, 5, v___f_61_);
return v___x_67_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack(void){
_start:
{
lean_object* v___x_68_; 
v___x_68_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack___closed__6);
return v___x_68_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt_decEq(lean_object* v_x_69_, lean_object* v_x_70_){
_start:
{
lean_object* v_re_71_; lean_object* v_im_72_; lean_object* v_re_73_; lean_object* v_im_74_; uint8_t v___x_75_; 
v_re_71_ = lean_ctor_get(v_x_69_, 0);
v_im_72_ = lean_ctor_get(v_x_69_, 1);
v_re_73_ = lean_ctor_get(v_x_70_, 0);
v_im_74_ = lean_ctor_get(v_x_70_, 1);
v___x_75_ = lean_int_dec_eq(v_re_71_, v_re_73_);
if (v___x_75_ == 0)
{
return v___x_75_;
}
else
{
uint8_t v___x_76_; 
v___x_76_ = lean_int_dec_eq(v_im_72_, v_im_74_);
return v___x_76_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt_decEq___boxed(lean_object* v_x_77_, lean_object* v_x_78_){
_start:
{
uint8_t v_res_79_; lean_object* v_r_80_; 
v_res_79_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt_decEq(v_x_77_, v_x_78_);
lean_dec_ref(v_x_78_);
lean_dec_ref(v_x_77_);
v_r_80_ = lean_box(v_res_79_);
return v_r_80_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt(lean_object* v_x_81_, lean_object* v_x_82_){
_start:
{
uint8_t v___x_83_; 
v___x_83_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt_decEq(v_x_81_, v_x_82_);
return v___x_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt___boxed(lean_object* v_x_84_, lean_object* v_x_85_){
_start:
{
uint8_t v_res_86_; lean_object* v_r_87_; 
v_res_86_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instDecidableEqGaussInt(v_x_84_, v_x_85_);
lean_dec_ref(v_x_85_);
lean_dec_ref(v_x_84_);
v_r_87_ = lean_box(v_res_86_);
return v_r_87_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_101_; lean_object* v___x_102_; 
v___x_101_ = lean_unsigned_to_nat(6u);
v___x_102_ = lean_nat_to_int(v___x_101_);
return v___x_102_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_104_; lean_object* v___x_105_; 
v___x_104_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__0));
v___x_105_ = lean_string_length(v___x_104_);
return v___x_105_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_106_; lean_object* v___x_107_; 
v___x_106_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__9);
v___x_107_ = lean_nat_to_int(v___x_106_);
return v___x_107_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg(lean_object* v_x_118_){
_start:
{
lean_object* v_re_119_; lean_object* v_im_120_; lean_object* v___x_122_; uint8_t v_isShared_123_; uint8_t v_isSharedCheck_172_; 
v_re_119_ = lean_ctor_get(v_x_118_, 0);
v_im_120_ = lean_ctor_get(v_x_118_, 1);
v_isSharedCheck_172_ = !lean_is_exclusive(v_x_118_);
if (v_isSharedCheck_172_ == 0)
{
v___x_122_ = v_x_118_;
v_isShared_123_ = v_isSharedCheck_172_;
goto v_resetjp_121_;
}
else
{
lean_inc(v_im_120_);
lean_inc(v_re_119_);
lean_dec(v_x_118_);
v___x_122_ = lean_box(0);
v_isShared_123_ = v_isSharedCheck_172_;
goto v_resetjp_121_;
}
v_resetjp_121_:
{
lean_object* v___x_124_; lean_object* v___x_125_; lean_object* v___x_126_; uint8_t v___y_128_; lean_object* v___y_129_; lean_object* v___y_130_; lean_object* v___y_144_; lean_object* v___x_164_; lean_object* v___x_165_; uint8_t v___x_166_; 
v___x_124_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__5));
v___x_125_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__6));
v___x_126_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__7);
v___x_164_ = lean_unsigned_to_nat(0u);
v___x_165_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4);
v___x_166_ = lean_int_dec_lt(v_re_119_, v___x_165_);
if (v___x_166_ == 0)
{
lean_object* v___x_167_; lean_object* v___x_168_; 
v___x_167_ = l_Int_repr(v_re_119_);
lean_dec(v_re_119_);
v___x_168_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_168_, 0, v___x_167_);
v___y_144_ = v___x_168_;
goto v___jp_143_;
}
else
{
lean_object* v___x_169_; lean_object* v___x_170_; lean_object* v___x_171_; 
v___x_169_ = l_Int_repr(v_re_119_);
lean_dec(v_re_119_);
v___x_170_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_170_, 0, v___x_169_);
v___x_171_ = l_Repr_addAppParen(v___x_170_, v___x_164_);
v___y_144_ = v___x_171_;
goto v___jp_143_;
}
v___jp_127_:
{
lean_object* v___x_132_; 
if (v_isShared_123_ == 0)
{
lean_ctor_set_tag(v___x_122_, 4);
lean_ctor_set(v___x_122_, 1, v___y_130_);
lean_ctor_set(v___x_122_, 0, v___x_126_);
v___x_132_ = v___x_122_;
goto v_reusejp_131_;
}
else
{
lean_object* v_reuseFailAlloc_142_; 
v_reuseFailAlloc_142_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_142_, 0, v___x_126_);
lean_ctor_set(v_reuseFailAlloc_142_, 1, v___y_130_);
v___x_132_ = v_reuseFailAlloc_142_;
goto v_reusejp_131_;
}
v_reusejp_131_:
{
lean_object* v___x_133_; lean_object* v___x_134_; lean_object* v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; lean_object* v___x_138_; lean_object* v___x_139_; lean_object* v___x_140_; lean_object* v___x_141_; 
v___x_133_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_133_, 0, v___x_132_);
lean_ctor_set_uint8(v___x_133_, sizeof(void*)*1, v___y_128_);
v___x_134_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_134_, 0, v___y_129_);
lean_ctor_set(v___x_134_, 1, v___x_133_);
v___x_135_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__10);
v___x_136_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__11));
v___x_137_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_137_, 0, v___x_136_);
lean_ctor_set(v___x_137_, 1, v___x_134_);
v___x_138_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__12));
v___x_139_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_139_, 0, v___x_137_);
lean_ctor_set(v___x_139_, 1, v___x_138_);
v___x_140_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_140_, 0, v___x_135_);
lean_ctor_set(v___x_140_, 1, v___x_139_);
v___x_141_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_141_, 0, v___x_140_);
lean_ctor_set_uint8(v___x_141_, sizeof(void*)*1, v___y_128_);
return v___x_141_;
}
}
v___jp_143_:
{
lean_object* v___x_145_; uint8_t v___x_146_; lean_object* v___x_147_; lean_object* v___x_148_; lean_object* v___x_149_; lean_object* v___x_150_; lean_object* v___x_151_; lean_object* v___x_152_; lean_object* v___x_153_; lean_object* v___x_154_; lean_object* v___x_155_; lean_object* v___x_156_; lean_object* v___x_157_; uint8_t v___x_158_; 
v___x_145_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_145_, 0, v___x_126_);
lean_ctor_set(v___x_145_, 1, v___y_144_);
v___x_146_ = 0;
v___x_147_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_147_, 0, v___x_145_);
lean_ctor_set_uint8(v___x_147_, sizeof(void*)*1, v___x_146_);
v___x_148_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_148_, 0, v___x_125_);
lean_ctor_set(v___x_148_, 1, v___x_147_);
v___x_149_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__14));
v___x_150_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_150_, 0, v___x_148_);
lean_ctor_set(v___x_150_, 1, v___x_149_);
v___x_151_ = lean_box(1);
v___x_152_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_152_, 0, v___x_150_);
lean_ctor_set(v___x_152_, 1, v___x_151_);
v___x_153_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg___closed__16));
v___x_154_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_154_, 0, v___x_152_);
lean_ctor_set(v___x_154_, 1, v___x_153_);
v___x_155_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_155_, 0, v___x_154_);
lean_ctor_set(v___x_155_, 1, v___x_124_);
v___x_156_ = lean_unsigned_to_nat(0u);
v___x_157_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4);
v___x_158_ = lean_int_dec_lt(v_im_120_, v___x_157_);
if (v___x_158_ == 0)
{
lean_object* v___x_159_; lean_object* v___x_160_; 
v___x_159_ = l_Int_repr(v_im_120_);
lean_dec(v_im_120_);
v___x_160_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_160_, 0, v___x_159_);
v___y_128_ = v___x_146_;
v___y_129_ = v___x_155_;
v___y_130_ = v___x_160_;
goto v___jp_127_;
}
else
{
lean_object* v___x_161_; lean_object* v___x_162_; lean_object* v___x_163_; 
v___x_161_ = l_Int_repr(v_im_120_);
lean_dec(v_im_120_);
v___x_162_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_162_, 0, v___x_161_);
v___x_163_ = l_Repr_addAppParen(v___x_162_, v___x_156_);
v___y_128_ = v___x_146_;
v___y_129_ = v___x_155_;
v___y_130_ = v___x_163_;
goto v___jp_127_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr(lean_object* v_x_173_, lean_object* v_prec_174_){
_start:
{
lean_object* v___x_175_; 
v___x_175_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___redArg(v_x_173_);
return v___x_175_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr___boxed(lean_object* v_x_176_, lean_object* v_prec_177_){
_start:
{
lean_object* v_res_178_; 
v_res_178_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_instReprGaussInt_repr(v_x_176_, v_prec_177_);
lean_dec(v_prec_177_);
return v_res_178_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd(lean_object* v_x_181_, lean_object* v_y_182_){
_start:
{
lean_object* v_re_183_; lean_object* v_im_184_; lean_object* v_re_185_; lean_object* v_im_186_; lean_object* v___x_188_; uint8_t v_isShared_189_; uint8_t v_isSharedCheck_195_; 
v_re_183_ = lean_ctor_get(v_x_181_, 0);
v_im_184_ = lean_ctor_get(v_x_181_, 1);
v_re_185_ = lean_ctor_get(v_y_182_, 0);
v_im_186_ = lean_ctor_get(v_y_182_, 1);
v_isSharedCheck_195_ = !lean_is_exclusive(v_y_182_);
if (v_isSharedCheck_195_ == 0)
{
v___x_188_ = v_y_182_;
v_isShared_189_ = v_isSharedCheck_195_;
goto v_resetjp_187_;
}
else
{
lean_inc(v_im_186_);
lean_inc(v_re_185_);
lean_dec(v_y_182_);
v___x_188_ = lean_box(0);
v_isShared_189_ = v_isSharedCheck_195_;
goto v_resetjp_187_;
}
v_resetjp_187_:
{
lean_object* v___x_190_; lean_object* v___x_191_; lean_object* v___x_193_; 
v___x_190_ = lean_int_add(v_re_183_, v_re_185_);
lean_dec(v_re_185_);
v___x_191_ = lean_int_add(v_im_184_, v_im_186_);
lean_dec(v_im_186_);
if (v_isShared_189_ == 0)
{
lean_ctor_set(v___x_188_, 1, v___x_191_);
lean_ctor_set(v___x_188_, 0, v___x_190_);
v___x_193_ = v___x_188_;
goto v_reusejp_192_;
}
else
{
lean_object* v_reuseFailAlloc_194_; 
v_reuseFailAlloc_194_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_194_, 0, v___x_190_);
lean_ctor_set(v_reuseFailAlloc_194_, 1, v___x_191_);
v___x_193_ = v_reuseFailAlloc_194_;
goto v_reusejp_192_;
}
v_reusejp_192_:
{
return v___x_193_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd___boxed(lean_object* v_x_196_, lean_object* v_y_197_){
_start:
{
lean_object* v_res_198_; 
v_res_198_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd(v_x_196_, v_y_197_);
lean_dec_ref(v_x_196_);
return v_res_198_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(lean_object* v_x_199_, lean_object* v_y_200_){
_start:
{
lean_object* v_re_201_; lean_object* v_im_202_; lean_object* v_re_203_; lean_object* v_im_204_; lean_object* v___x_206_; uint8_t v_isShared_207_; uint8_t v_isSharedCheck_217_; 
v_re_201_ = lean_ctor_get(v_x_199_, 0);
v_im_202_ = lean_ctor_get(v_x_199_, 1);
v_re_203_ = lean_ctor_get(v_y_200_, 0);
v_im_204_ = lean_ctor_get(v_y_200_, 1);
v_isSharedCheck_217_ = !lean_is_exclusive(v_y_200_);
if (v_isSharedCheck_217_ == 0)
{
v___x_206_ = v_y_200_;
v_isShared_207_ = v_isSharedCheck_217_;
goto v_resetjp_205_;
}
else
{
lean_inc(v_im_204_);
lean_inc(v_re_203_);
lean_dec(v_y_200_);
v___x_206_ = lean_box(0);
v_isShared_207_ = v_isSharedCheck_217_;
goto v_resetjp_205_;
}
v_resetjp_205_:
{
lean_object* v___x_208_; lean_object* v___x_209_; lean_object* v___x_210_; lean_object* v___x_211_; lean_object* v___x_212_; lean_object* v___x_213_; lean_object* v___x_215_; 
v___x_208_ = lean_int_mul(v_re_201_, v_re_203_);
v___x_209_ = lean_int_mul(v_im_202_, v_im_204_);
v___x_210_ = lean_int_sub(v___x_208_, v___x_209_);
lean_dec(v___x_209_);
lean_dec(v___x_208_);
v___x_211_ = lean_int_mul(v_re_201_, v_im_204_);
lean_dec(v_im_204_);
v___x_212_ = lean_int_mul(v_im_202_, v_re_203_);
lean_dec(v_re_203_);
v___x_213_ = lean_int_add(v___x_211_, v___x_212_);
lean_dec(v___x_212_);
lean_dec(v___x_211_);
if (v_isShared_207_ == 0)
{
lean_ctor_set(v___x_206_, 1, v___x_213_);
lean_ctor_set(v___x_206_, 0, v___x_210_);
v___x_215_ = v___x_206_;
goto v_reusejp_214_;
}
else
{
lean_object* v_reuseFailAlloc_216_; 
v_reuseFailAlloc_216_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_216_, 0, v___x_210_);
lean_ctor_set(v_reuseFailAlloc_216_, 1, v___x_213_);
v___x_215_ = v_reuseFailAlloc_216_;
goto v_reusejp_214_;
}
v_reusejp_214_:
{
return v___x_215_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul___boxed(lean_object* v_x_218_, lean_object* v_y_219_){
_start:
{
lean_object* v_res_220_; 
v_res_220_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(v_x_218_, v_y_219_);
lean_dec_ref(v_x_218_);
return v_res_220_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(lean_object* v_x_221_){
_start:
{
lean_object* v_re_222_; lean_object* v_im_223_; lean_object* v___x_225_; uint8_t v_isShared_226_; uint8_t v_isSharedCheck_232_; 
v_re_222_ = lean_ctor_get(v_x_221_, 0);
v_im_223_ = lean_ctor_get(v_x_221_, 1);
v_isSharedCheck_232_ = !lean_is_exclusive(v_x_221_);
if (v_isSharedCheck_232_ == 0)
{
v___x_225_ = v_x_221_;
v_isShared_226_ = v_isSharedCheck_232_;
goto v_resetjp_224_;
}
else
{
lean_inc(v_im_223_);
lean_inc(v_re_222_);
lean_dec(v_x_221_);
v___x_225_ = lean_box(0);
v_isShared_226_ = v_isSharedCheck_232_;
goto v_resetjp_224_;
}
v_resetjp_224_:
{
lean_object* v___x_227_; lean_object* v___x_228_; lean_object* v___x_230_; 
v___x_227_ = lean_int_neg(v_re_222_);
lean_dec(v_re_222_);
v___x_228_ = lean_int_neg(v_im_223_);
lean_dec(v_im_223_);
if (v_isShared_226_ == 0)
{
lean_ctor_set(v___x_225_, 1, v___x_228_);
lean_ctor_set(v___x_225_, 0, v___x_227_);
v___x_230_ = v___x_225_;
goto v_reusejp_229_;
}
else
{
lean_object* v_reuseFailAlloc_231_; 
v_reuseFailAlloc_231_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_231_, 0, v___x_227_);
lean_ctor_set(v_reuseFailAlloc_231_, 1, v___x_228_);
v___x_230_ = v_reuseFailAlloc_231_;
goto v_reusejp_229_;
}
v_reusejp_229_:
{
return v___x_230_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(lean_object* v_x_233_){
_start:
{
lean_object* v_re_234_; lean_object* v_im_235_; lean_object* v___x_237_; uint8_t v_isShared_238_; uint8_t v_isSharedCheck_243_; 
v_re_234_ = lean_ctor_get(v_x_233_, 0);
v_im_235_ = lean_ctor_get(v_x_233_, 1);
v_isSharedCheck_243_ = !lean_is_exclusive(v_x_233_);
if (v_isSharedCheck_243_ == 0)
{
v___x_237_ = v_x_233_;
v_isShared_238_ = v_isSharedCheck_243_;
goto v_resetjp_236_;
}
else
{
lean_inc(v_im_235_);
lean_inc(v_re_234_);
lean_dec(v_x_233_);
v___x_237_ = lean_box(0);
v_isShared_238_ = v_isSharedCheck_243_;
goto v_resetjp_236_;
}
v_resetjp_236_:
{
lean_object* v___x_239_; lean_object* v___x_241_; 
v___x_239_ = lean_int_neg(v_im_235_);
lean_dec(v_im_235_);
if (v_isShared_238_ == 0)
{
lean_ctor_set(v___x_237_, 1, v___x_239_);
v___x_241_ = v___x_237_;
goto v_reusejp_240_;
}
else
{
lean_object* v_reuseFailAlloc_242_; 
v_reuseFailAlloc_242_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_242_, 0, v_re_234_);
lean_ctor_set(v_reuseFailAlloc_242_, 1, v___x_239_);
v___x_241_ = v_reuseFailAlloc_242_;
goto v_reusejp_240_;
}
v_reusejp_240_:
{
return v___x_241_;
}
}
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero___closed__0(void){
_start:
{
lean_object* v___x_244_; lean_object* v___x_245_; 
v___x_244_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4);
v___x_245_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_245_, 0, v___x_244_);
lean_ctor_set(v___x_245_, 1, v___x_244_);
return v___x_245_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero(void){
_start:
{
lean_object* v___x_246_; 
v___x_246_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero___closed__0);
return v___x_246_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone___closed__0(void){
_start:
{
lean_object* v___x_247_; lean_object* v___x_248_; lean_object* v___x_249_; 
v___x_247_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4);
v___x_248_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5);
v___x_249_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_249_, 0, v___x_248_);
lean_ctor_set(v___x_249_, 1, v___x_247_);
return v___x_249_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone(void){
_start:
{
lean_object* v___x_250_; 
v___x_250_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone___closed__0);
return v___x_250_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi___closed__0(void){
_start:
{
lean_object* v___x_251_; lean_object* v___x_252_; lean_object* v___x_253_; 
v___x_251_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__5);
v___x_252_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack___closed__4);
v___x_253_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_253_, 0, v___x_252_);
lean_ctor_set(v___x_253_, 1, v___x_251_);
return v___x_253_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi(void){
_start:
{
lean_object* v___x_254_; 
v___x_254_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi___closed__0);
return v___x_254_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__4(void){
_start:
{
lean_object* v___x_259_; lean_object* v___x_260_; lean_object* v___x_261_; lean_object* v___x_262_; lean_object* v___x_263_; lean_object* v___x_264_; lean_object* v___x_265_; 
v___x_259_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__3));
v___x_260_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
v___x_261_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
v___x_262_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__2));
v___x_263_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__1));
v___x_264_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__0));
v___x_265_ = lean_alloc_ctor(0, 6, 0);
lean_ctor_set(v___x_265_, 0, v___x_264_);
lean_ctor_set(v___x_265_, 1, v___x_263_);
lean_ctor_set(v___x_265_, 2, v___x_262_);
lean_ctor_set(v___x_265_, 3, v___x_261_);
lean_ctor_set(v___x_265_, 4, v___x_260_);
lean_ctor_set(v___x_265_, 5, v___x_259_);
return v___x_265_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack(void){
_start:
{
lean_object* v___x_266_; 
v___x_266_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack___closed__4);
return v___x_266_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__0(uint8_t v_x_267_, uint8_t v_y_268_){
_start:
{
if (v_x_267_ == 0)
{
return v_x_267_;
}
else
{
return v_y_268_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__0___boxed(lean_object* v_x_269_, lean_object* v_y_270_){
_start:
{
uint8_t v_x_boxed_271_; uint8_t v_y_boxed_272_; uint8_t v_res_273_; lean_object* v_r_274_; 
v_x_boxed_271_ = lean_unbox(v_x_269_);
v_y_boxed_272_ = lean_unbox(v_y_270_);
v_res_273_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__0(v_x_boxed_271_, v_y_boxed_272_);
v_r_274_ = lean_box(v_res_273_);
return v_r_274_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__1(uint8_t v___y_275_, uint8_t v___y_276_){
_start:
{
if (v___y_275_ == 0)
{
return v___y_276_;
}
else
{
if (v___y_276_ == 0)
{
return v___y_275_;
}
else
{
uint8_t v___x_277_; 
v___x_277_ = 0;
return v___x_277_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__1___boxed(lean_object* v___y_278_, lean_object* v___y_279_){
_start:
{
uint8_t v___y_46__boxed_280_; uint8_t v___y_47__boxed_281_; uint8_t v_res_282_; lean_object* v_r_283_; 
v___y_46__boxed_280_ = lean_unbox(v___y_278_);
v___y_47__boxed_281_ = lean_unbox(v___y_279_);
v_res_282_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__1(v___y_46__boxed_280_, v___y_47__boxed_281_);
v_r_283_ = lean_box(v_res_282_);
return v_r_283_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__2(uint8_t v___y_284_){
_start:
{
return v___y_284_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__2___boxed(lean_object* v___y_285_){
_start:
{
uint8_t v___y_54__boxed_286_; uint8_t v_res_287_; lean_object* v_r_288_; 
v___y_54__boxed_286_ = lean_unbox(v___y_285_);
v_res_287_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack___lam__2(v___y_54__boxed_286_);
v_r_288_ = lean_box(v_res_287_);
return v_r_288_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack = _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack);
lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack = _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_ratPack);
lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero = _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero);
lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone = _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone);
lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi = _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi);
lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack = _init_lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
