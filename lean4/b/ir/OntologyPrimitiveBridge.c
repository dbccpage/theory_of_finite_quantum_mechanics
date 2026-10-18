// Lean compiler output
// Module: OntologyPrimitiveBridge
// Imports: public import Init public meta import Init public import OntologyBasic public import PrimitiveTerminalPacket
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
static const lean_string_object lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_paper000cClaimPacketEvidenceId___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "PAPER000C-CLAIM-PACKET-AUTHORITY-BOUNDARY"};
static const lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_paper000cClaimPacketEvidenceId___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_paper000cClaimPacketEvidenceId___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_paper000cClaimPacketEvidenceId = (const lean_object*)&lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_paper000cClaimPacketEvidenceId___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___redArg___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal___redArg___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter___redArg(uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter(lean_object*, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter___redArg(uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter(lean_object*, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___redArg(lean_object* v_packet_3_){
_start:
{
uint8_t v_boundary_4_; 
v_boundary_4_ = lean_ctor_get_uint8(v_packet_3_, 1);
switch(v_boundary_4_)
{
case 0:
{
uint8_t v_hasCertificate_5_; 
v_hasCertificate_5_ = lean_ctor_get_uint8(v_packet_3_, 2);
if (v_hasCertificate_5_ == 0)
{
uint8_t v___x_6_; 
v___x_6_ = 5;
return v___x_6_;
}
else
{
uint8_t v___x_7_; 
v___x_7_ = 1;
return v___x_7_;
}
}
case 1:
{
uint8_t v_status_8_; 
v_status_8_ = lean_ctor_get_uint8(v_packet_3_, 0);
switch(v_status_8_)
{
case 0:
{
uint8_t v_hasCertificate_9_; 
v_hasCertificate_9_ = lean_ctor_get_uint8(v_packet_3_, 2);
if (v_hasCertificate_9_ == 0)
{
uint8_t v___x_10_; 
v___x_10_ = 5;
return v___x_10_;
}
else
{
uint8_t v___x_11_; 
v___x_11_ = 0;
return v___x_11_;
}
}
case 1:
{
uint8_t v_hasCertificate_12_; 
v_hasCertificate_12_ = lean_ctor_get_uint8(v_packet_3_, 2);
if (v_hasCertificate_12_ == 0)
{
uint8_t v___x_13_; 
v___x_13_ = 5;
return v___x_13_;
}
else
{
uint8_t v___x_14_; 
v___x_14_ = 3;
return v___x_14_;
}
}
default: 
{
uint8_t v___x_15_; 
v___x_15_ = 5;
return v___x_15_;
}
}
}
case 2:
{
uint8_t v___x_16_; 
v___x_16_ = 6;
return v___x_16_;
}
default: 
{
uint8_t v___x_17_; 
v___x_17_ = 4;
return v___x_17_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___redArg___boxed(lean_object* v_packet_18_){
_start:
{
uint8_t v_res_19_; lean_object* v_r_20_; 
v_res_19_ = lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___redArg(v_packet_18_);
lean_dec_ref(v_packet_18_);
v_r_20_ = lean_box(v_res_19_);
return v_r_20_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal(lean_object* v_Q_21_, lean_object* v_C_22_, lean_object* v_q_23_, lean_object* v_packet_24_){
_start:
{
uint8_t v___x_25_; 
v___x_25_ = lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___redArg(v_packet_24_);
return v___x_25_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___boxed(lean_object* v_Q_26_, lean_object* v_C_27_, lean_object* v_q_28_, lean_object* v_packet_29_){
_start:
{
uint8_t v_res_30_; lean_object* v_r_31_; 
v_res_30_ = lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal(v_Q_26_, v_C_27_, v_q_28_, v_packet_29_);
lean_dec_ref(v_packet_29_);
lean_dec(v_q_28_);
lean_dec_ref(v_C_27_);
v_r_31_ = lean_box(v_res_30_);
return v_r_31_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal___redArg(lean_object* v_packet_32_){
_start:
{
uint8_t v___x_33_; 
v___x_33_ = lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___redArg(v_packet_32_);
return v___x_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal___redArg___boxed(lean_object* v_packet_34_){
_start:
{
uint8_t v_res_35_; lean_object* v_r_36_; 
v_res_35_ = lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal___redArg(v_packet_34_);
lean_dec_ref(v_packet_34_);
v_r_36_ = lean_box(v_res_35_);
return v_r_36_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal(lean_object* v_Q_37_, lean_object* v_C_38_, lean_object* v_q_39_, lean_object* v_packet_40_, lean_object* v_descendsToPrimitiveDifference_41_, lean_object* v_descendsToStructure_42_){
_start:
{
uint8_t v___x_43_; 
v___x_43_ = lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_statusFromPrimitiveTerminal___redArg(v_packet_40_);
return v___x_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal___boxed(lean_object* v_Q_44_, lean_object* v_C_45_, lean_object* v_q_46_, lean_object* v_packet_47_, lean_object* v_descendsToPrimitiveDifference_48_, lean_object* v_descendsToStructure_49_){
_start:
{
uint8_t v_res_50_; lean_object* v_r_51_; 
v_res_50_ = lp_FiniteQuantum_OmegaCosmology_Ontology_PrimitiveBridge_claimPacketFromPrimitiveTerminal(v_Q_44_, v_C_45_, v_q_46_, v_packet_47_, v_descendsToPrimitiveDifference_48_, v_descendsToStructure_49_);
lean_dec_ref(v_packet_47_);
lean_dec(v_q_46_);
lean_dec_ref(v_C_45_);
v_r_51_ = lean_box(v_res_50_);
return v_r_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter___redArg(uint8_t v_x_52_, lean_object* v_h__1_53_, lean_object* v_h__2_54_, lean_object* v_h__3_55_, lean_object* v_h__4_56_, lean_object* v_h__5_57_, lean_object* v_h__6_58_, lean_object* v_h__7_59_){
_start:
{
switch(v_x_52_)
{
case 0:
{
lean_object* v___x_60_; lean_object* v___x_61_; 
lean_dec(v_h__7_59_);
lean_dec(v_h__6_58_);
lean_dec(v_h__5_57_);
lean_dec(v_h__4_56_);
lean_dec(v_h__3_55_);
lean_dec(v_h__2_54_);
v___x_60_ = lean_box(0);
v___x_61_ = lean_apply_1(v_h__1_53_, v___x_60_);
return v___x_61_;
}
case 1:
{
lean_object* v___x_62_; lean_object* v___x_63_; 
lean_dec(v_h__7_59_);
lean_dec(v_h__6_58_);
lean_dec(v_h__5_57_);
lean_dec(v_h__4_56_);
lean_dec(v_h__3_55_);
lean_dec(v_h__1_53_);
v___x_62_ = lean_box(0);
v___x_63_ = lean_apply_1(v_h__2_54_, v___x_62_);
return v___x_63_;
}
case 2:
{
lean_object* v___x_64_; lean_object* v___x_65_; 
lean_dec(v_h__7_59_);
lean_dec(v_h__6_58_);
lean_dec(v_h__5_57_);
lean_dec(v_h__4_56_);
lean_dec(v_h__2_54_);
lean_dec(v_h__1_53_);
v___x_64_ = lean_box(0);
v___x_65_ = lean_apply_1(v_h__3_55_, v___x_64_);
return v___x_65_;
}
case 3:
{
lean_object* v___x_66_; lean_object* v___x_67_; 
lean_dec(v_h__7_59_);
lean_dec(v_h__6_58_);
lean_dec(v_h__5_57_);
lean_dec(v_h__3_55_);
lean_dec(v_h__2_54_);
lean_dec(v_h__1_53_);
v___x_66_ = lean_box(0);
v___x_67_ = lean_apply_1(v_h__4_56_, v___x_66_);
return v___x_67_;
}
case 4:
{
lean_object* v___x_68_; lean_object* v___x_69_; 
lean_dec(v_h__7_59_);
lean_dec(v_h__6_58_);
lean_dec(v_h__4_56_);
lean_dec(v_h__3_55_);
lean_dec(v_h__2_54_);
lean_dec(v_h__1_53_);
v___x_68_ = lean_box(0);
v___x_69_ = lean_apply_1(v_h__5_57_, v___x_68_);
return v___x_69_;
}
case 5:
{
lean_object* v___x_70_; lean_object* v___x_71_; 
lean_dec(v_h__7_59_);
lean_dec(v_h__5_57_);
lean_dec(v_h__4_56_);
lean_dec(v_h__3_55_);
lean_dec(v_h__2_54_);
lean_dec(v_h__1_53_);
v___x_70_ = lean_box(0);
v___x_71_ = lean_apply_1(v_h__6_58_, v___x_70_);
return v___x_71_;
}
default: 
{
lean_object* v___x_72_; lean_object* v___x_73_; 
lean_dec(v_h__6_58_);
lean_dec(v_h__5_57_);
lean_dec(v_h__4_56_);
lean_dec(v_h__3_55_);
lean_dec(v_h__2_54_);
lean_dec(v_h__1_53_);
v___x_72_ = lean_box(0);
v___x_73_ = lean_apply_1(v_h__7_59_, v___x_72_);
return v___x_73_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter___redArg___boxed(lean_object* v_x_74_, lean_object* v_h__1_75_, lean_object* v_h__2_76_, lean_object* v_h__3_77_, lean_object* v_h__4_78_, lean_object* v_h__5_79_, lean_object* v_h__6_80_, lean_object* v_h__7_81_){
_start:
{
uint8_t v_x_69__boxed_82_; lean_object* v_res_83_; 
v_x_69__boxed_82_ = lean_unbox(v_x_74_);
v_res_83_ = lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter___redArg(v_x_69__boxed_82_, v_h__1_75_, v_h__2_76_, v_h__3_77_, v_h__4_78_, v_h__5_79_, v_h__6_80_, v_h__7_81_);
return v_res_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter(lean_object* v_motive_84_, uint8_t v_x_85_, lean_object* v_h__1_86_, lean_object* v_h__2_87_, lean_object* v_h__3_88_, lean_object* v_h__4_89_, lean_object* v_h__5_90_, lean_object* v_h__6_91_, lean_object* v_h__7_92_){
_start:
{
switch(v_x_85_)
{
case 0:
{
lean_object* v___x_93_; lean_object* v___x_94_; 
lean_dec(v_h__7_92_);
lean_dec(v_h__6_91_);
lean_dec(v_h__5_90_);
lean_dec(v_h__4_89_);
lean_dec(v_h__3_88_);
lean_dec(v_h__2_87_);
v___x_93_ = lean_box(0);
v___x_94_ = lean_apply_1(v_h__1_86_, v___x_93_);
return v___x_94_;
}
case 1:
{
lean_object* v___x_95_; lean_object* v___x_96_; 
lean_dec(v_h__7_92_);
lean_dec(v_h__6_91_);
lean_dec(v_h__5_90_);
lean_dec(v_h__4_89_);
lean_dec(v_h__3_88_);
lean_dec(v_h__1_86_);
v___x_95_ = lean_box(0);
v___x_96_ = lean_apply_1(v_h__2_87_, v___x_95_);
return v___x_96_;
}
case 2:
{
lean_object* v___x_97_; lean_object* v___x_98_; 
lean_dec(v_h__7_92_);
lean_dec(v_h__6_91_);
lean_dec(v_h__5_90_);
lean_dec(v_h__4_89_);
lean_dec(v_h__2_87_);
lean_dec(v_h__1_86_);
v___x_97_ = lean_box(0);
v___x_98_ = lean_apply_1(v_h__3_88_, v___x_97_);
return v___x_98_;
}
case 3:
{
lean_object* v___x_99_; lean_object* v___x_100_; 
lean_dec(v_h__7_92_);
lean_dec(v_h__6_91_);
lean_dec(v_h__5_90_);
lean_dec(v_h__3_88_);
lean_dec(v_h__2_87_);
lean_dec(v_h__1_86_);
v___x_99_ = lean_box(0);
v___x_100_ = lean_apply_1(v_h__4_89_, v___x_99_);
return v___x_100_;
}
case 4:
{
lean_object* v___x_101_; lean_object* v___x_102_; 
lean_dec(v_h__7_92_);
lean_dec(v_h__6_91_);
lean_dec(v_h__4_89_);
lean_dec(v_h__3_88_);
lean_dec(v_h__2_87_);
lean_dec(v_h__1_86_);
v___x_101_ = lean_box(0);
v___x_102_ = lean_apply_1(v_h__5_90_, v___x_101_);
return v___x_102_;
}
case 5:
{
lean_object* v___x_103_; lean_object* v___x_104_; 
lean_dec(v_h__7_92_);
lean_dec(v_h__5_90_);
lean_dec(v_h__4_89_);
lean_dec(v_h__3_88_);
lean_dec(v_h__2_87_);
lean_dec(v_h__1_86_);
v___x_103_ = lean_box(0);
v___x_104_ = lean_apply_1(v_h__6_91_, v___x_103_);
return v___x_104_;
}
default: 
{
lean_object* v___x_105_; lean_object* v___x_106_; 
lean_dec(v_h__6_91_);
lean_dec(v_h__5_90_);
lean_dec(v_h__4_89_);
lean_dec(v_h__3_88_);
lean_dec(v_h__2_87_);
lean_dec(v_h__1_86_);
v___x_105_ = lean_box(0);
v___x_106_ = lean_apply_1(v_h__7_92_, v___x_105_);
return v___x_106_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter___boxed(lean_object* v_motive_107_, lean_object* v_x_108_, lean_object* v_h__1_109_, lean_object* v_h__2_110_, lean_object* v_h__3_111_, lean_object* v_h__4_112_, lean_object* v_h__5_113_, lean_object* v_h__6_114_, lean_object* v_h__7_115_){
_start:
{
uint8_t v_x_100__boxed_116_; lean_object* v_res_117_; 
v_x_100__boxed_116_ = lean_unbox(v_x_108_);
v_res_117_ = lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_Authoritative_match__1_splitter(v_motive_107_, v_x_100__boxed_116_, v_h__1_109_, v_h__2_110_, v_h__3_111_, v_h__4_112_, v_h__5_113_, v_h__6_114_, v_h__7_115_);
return v_res_117_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter___redArg(uint8_t v_x_118_, lean_object* v_h__1_119_, lean_object* v_h__2_120_, lean_object* v_h__3_121_, lean_object* v_h__4_122_, lean_object* v_h__5_123_, lean_object* v_h__6_124_, lean_object* v_h__7_125_){
_start:
{
switch(v_x_118_)
{
case 0:
{
lean_object* v___x_126_; lean_object* v___x_127_; 
lean_dec(v_h__7_125_);
lean_dec(v_h__6_124_);
lean_dec(v_h__5_123_);
lean_dec(v_h__3_121_);
lean_dec(v_h__2_120_);
lean_dec(v_h__1_119_);
v___x_126_ = lean_box(0);
v___x_127_ = lean_apply_1(v_h__4_122_, v___x_126_);
return v___x_127_;
}
case 1:
{
lean_object* v___x_128_; lean_object* v___x_129_; 
lean_dec(v_h__7_125_);
lean_dec(v_h__6_124_);
lean_dec(v_h__4_122_);
lean_dec(v_h__3_121_);
lean_dec(v_h__2_120_);
lean_dec(v_h__1_119_);
v___x_128_ = lean_box(0);
v___x_129_ = lean_apply_1(v_h__5_123_, v___x_128_);
return v___x_129_;
}
case 2:
{
lean_object* v___x_130_; lean_object* v___x_131_; 
lean_dec(v_h__7_125_);
lean_dec(v_h__5_123_);
lean_dec(v_h__4_122_);
lean_dec(v_h__3_121_);
lean_dec(v_h__2_120_);
lean_dec(v_h__1_119_);
v___x_130_ = lean_box(0);
v___x_131_ = lean_apply_1(v_h__6_124_, v___x_130_);
return v___x_131_;
}
case 3:
{
lean_object* v___x_132_; lean_object* v___x_133_; 
lean_dec(v_h__6_124_);
lean_dec(v_h__5_123_);
lean_dec(v_h__4_122_);
lean_dec(v_h__3_121_);
lean_dec(v_h__2_120_);
lean_dec(v_h__1_119_);
v___x_132_ = lean_box(0);
v___x_133_ = lean_apply_1(v_h__7_125_, v___x_132_);
return v___x_133_;
}
case 4:
{
lean_object* v___x_134_; lean_object* v___x_135_; 
lean_dec(v_h__7_125_);
lean_dec(v_h__6_124_);
lean_dec(v_h__5_123_);
lean_dec(v_h__4_122_);
lean_dec(v_h__3_121_);
lean_dec(v_h__2_120_);
v___x_134_ = lean_box(0);
v___x_135_ = lean_apply_1(v_h__1_119_, v___x_134_);
return v___x_135_;
}
case 5:
{
lean_object* v___x_136_; lean_object* v___x_137_; 
lean_dec(v_h__7_125_);
lean_dec(v_h__6_124_);
lean_dec(v_h__5_123_);
lean_dec(v_h__4_122_);
lean_dec(v_h__3_121_);
lean_dec(v_h__1_119_);
v___x_136_ = lean_box(0);
v___x_137_ = lean_apply_1(v_h__2_120_, v___x_136_);
return v___x_137_;
}
default: 
{
lean_object* v___x_138_; lean_object* v___x_139_; 
lean_dec(v_h__7_125_);
lean_dec(v_h__6_124_);
lean_dec(v_h__5_123_);
lean_dec(v_h__4_122_);
lean_dec(v_h__2_120_);
lean_dec(v_h__1_119_);
v___x_138_ = lean_box(0);
v___x_139_ = lean_apply_1(v_h__3_121_, v___x_138_);
return v___x_139_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter___redArg___boxed(lean_object* v_x_140_, lean_object* v_h__1_141_, lean_object* v_h__2_142_, lean_object* v_h__3_143_, lean_object* v_h__4_144_, lean_object* v_h__5_145_, lean_object* v_h__6_146_, lean_object* v_h__7_147_){
_start:
{
uint8_t v_x_69__boxed_148_; lean_object* v_res_149_; 
v_x_69__boxed_148_ = lean_unbox(v_x_140_);
v_res_149_ = lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter___redArg(v_x_69__boxed_148_, v_h__1_141_, v_h__2_142_, v_h__3_143_, v_h__4_144_, v_h__5_145_, v_h__6_146_, v_h__7_147_);
return v_res_149_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter(lean_object* v_motive_150_, uint8_t v_x_151_, lean_object* v_h__1_152_, lean_object* v_h__2_153_, lean_object* v_h__3_154_, lean_object* v_h__4_155_, lean_object* v_h__5_156_, lean_object* v_h__6_157_, lean_object* v_h__7_158_){
_start:
{
switch(v_x_151_)
{
case 0:
{
lean_object* v___x_159_; lean_object* v___x_160_; 
lean_dec(v_h__7_158_);
lean_dec(v_h__6_157_);
lean_dec(v_h__5_156_);
lean_dec(v_h__3_154_);
lean_dec(v_h__2_153_);
lean_dec(v_h__1_152_);
v___x_159_ = lean_box(0);
v___x_160_ = lean_apply_1(v_h__4_155_, v___x_159_);
return v___x_160_;
}
case 1:
{
lean_object* v___x_161_; lean_object* v___x_162_; 
lean_dec(v_h__7_158_);
lean_dec(v_h__6_157_);
lean_dec(v_h__4_155_);
lean_dec(v_h__3_154_);
lean_dec(v_h__2_153_);
lean_dec(v_h__1_152_);
v___x_161_ = lean_box(0);
v___x_162_ = lean_apply_1(v_h__5_156_, v___x_161_);
return v___x_162_;
}
case 2:
{
lean_object* v___x_163_; lean_object* v___x_164_; 
lean_dec(v_h__7_158_);
lean_dec(v_h__5_156_);
lean_dec(v_h__4_155_);
lean_dec(v_h__3_154_);
lean_dec(v_h__2_153_);
lean_dec(v_h__1_152_);
v___x_163_ = lean_box(0);
v___x_164_ = lean_apply_1(v_h__6_157_, v___x_163_);
return v___x_164_;
}
case 3:
{
lean_object* v___x_165_; lean_object* v___x_166_; 
lean_dec(v_h__6_157_);
lean_dec(v_h__5_156_);
lean_dec(v_h__4_155_);
lean_dec(v_h__3_154_);
lean_dec(v_h__2_153_);
lean_dec(v_h__1_152_);
v___x_165_ = lean_box(0);
v___x_166_ = lean_apply_1(v_h__7_158_, v___x_165_);
return v___x_166_;
}
case 4:
{
lean_object* v___x_167_; lean_object* v___x_168_; 
lean_dec(v_h__7_158_);
lean_dec(v_h__6_157_);
lean_dec(v_h__5_156_);
lean_dec(v_h__4_155_);
lean_dec(v_h__3_154_);
lean_dec(v_h__2_153_);
v___x_167_ = lean_box(0);
v___x_168_ = lean_apply_1(v_h__1_152_, v___x_167_);
return v___x_168_;
}
case 5:
{
lean_object* v___x_169_; lean_object* v___x_170_; 
lean_dec(v_h__7_158_);
lean_dec(v_h__6_157_);
lean_dec(v_h__5_156_);
lean_dec(v_h__4_155_);
lean_dec(v_h__3_154_);
lean_dec(v_h__1_152_);
v___x_169_ = lean_box(0);
v___x_170_ = lean_apply_1(v_h__2_153_, v___x_169_);
return v___x_170_;
}
default: 
{
lean_object* v___x_171_; lean_object* v___x_172_; 
lean_dec(v_h__7_158_);
lean_dec(v_h__6_157_);
lean_dec(v_h__5_156_);
lean_dec(v_h__4_155_);
lean_dec(v_h__2_153_);
lean_dec(v_h__1_152_);
v___x_171_ = lean_box(0);
v___x_172_ = lean_apply_1(v_h__3_154_, v___x_171_);
return v___x_172_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter___boxed(lean_object* v_motive_173_, lean_object* v_x_174_, lean_object* v_h__1_175_, lean_object* v_h__2_176_, lean_object* v_h__3_177_, lean_object* v_h__4_178_, lean_object* v_h__5_179_, lean_object* v_h__6_180_, lean_object* v_h__7_181_){
_start:
{
uint8_t v_x_100__boxed_182_; lean_object* v_res_183_; 
v_x_100__boxed_182_ = lean_unbox(v_x_174_);
v_res_183_ = lp_FiniteQuantum___private_OntologyPrimitiveBridge_0__OmegaCosmology_Ontology_TerminalStatus_TypedRefusal_match__1_splitter(v_motive_173_, v_x_100__boxed_182_, v_h__1_175_, v_h__2_176_, v_h__3_177_, v_h__4_178_, v_h__5_179_, v_h__6_180_, v_h__7_181_);
return v_res_183_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_OntologyBasic(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveTerminalPacket(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_OntologyPrimitiveBridge(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_OntologyBasic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveTerminalPacket(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
