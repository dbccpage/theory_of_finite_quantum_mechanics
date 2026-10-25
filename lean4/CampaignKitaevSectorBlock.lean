import Std
namespace CampaignKitaevSectorBlock
abbrev State := Bool → Bool → Int
def sign (g : Bool) : Int := if g then -1 else 1
def flux (v : State) : State := fun g b => sign g * v g b
def hopping (v : State) : State := fun g b => sign g * v g (!b)
def project (sector : Bool) (v : State) : State := fun g b => if g = sector then v g b else 0

theorem flux_involution (v : State) : flux (flux v) = v := by
  funext g b; cases g <;> simp [flux, sign]

theorem hopping_involution (v : State) : hopping (hopping v) = v := by
  funext g b; cases g <;> cases b <;> simp [hopping, sign]

theorem flux_commutes_hopping (v : State) : flux (hopping v) = hopping (flux v) := by
  rfl

theorem project_commutes_hopping (sector : Bool) (v : State) :
    project sector (hopping v) = hopping (project sector v) := by
  funext g b; cases sector <;> cases g <;> simp [project, hopping, sign]

theorem sector_decomposition (v : State) (g b : Bool) :
    project false v g b + project true v g b = v g b := by
  cases g <;> simp [project]

theorem restricted_hopping (v : State) (g b : Bool) :
    hopping v g b = sign g * v g (!b) := rfl

theorem sectors_distinct : sign false ≠ sign true := by decide
end CampaignKitaevSectorBlock
#print axioms CampaignKitaevSectorBlock.flux_involution
#print axioms CampaignKitaevSectorBlock.hopping_involution
#print axioms CampaignKitaevSectorBlock.flux_commutes_hopping
#print axioms CampaignKitaevSectorBlock.project_commutes_hopping
#print axioms CampaignKitaevSectorBlock.sector_decomposition
#print axioms CampaignKitaevSectorBlock.restricted_hopping
#print axioms CampaignKitaevSectorBlock.sectors_distinct
