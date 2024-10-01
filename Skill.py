class Skill:
    all_skills = []
    
    def __init__(self, name):
        self.name = name
        self.dependencies = []

    def add_dependency(self, skill, level):
        d = {'skill': skill, 'level': level}
        self.dependencies.append(d)
        
    @staticmethod
    def string_to_skill(name):
        s = next((x for x in Skill.all_skills if x.name == name), 'ERROR')
        if s == 'ERROR':
            raise ValueError(f'Skill {name} not a valid skill')
        return s


patt = Skill('PATT')
Skill.all_skills.append(patt)

forc = Skill('FORC')
Skill.all_skills.append(forc)

spir = Skill('SPIR')
Skill.all_skills.append(spir)

fire = Skill('FIRE')
fire.add_dependency(forc, 1)
Skill.all_skills.append(fire)

equa = Skill('EQUA')
equa.add_dependency(forc, 1)
equa.add_dependency(patt, 1)
Skill.all_skills.append(equa)

fshi = Skill('FSHI')
fshi.add_dependency(forc, 1)
Skill.all_skills.append(fshi)

eshi = Skill('ESHI')
eshi.add_dependency(forc, 1)
Skill.all_skills.append(eshi)

sshi = Skill('SSHI')
sshi.add_dependency(forc, 1)
sshi.add_dependency(spir, 1)
Skill.all_skills.append(sshi)

mhea = Skill('MHEA')
mhea.add_dependency(patt, 1)
Skill.all_skills.append(mhea)

gate = Skill('GATE')
gate.add_dependency(patt, 1)
gate.add_dependency(spir, 1)
Skill.all_skills.append(gate)

fars = Skill('FARS')
fars.add_dependency(patt, 1)
fars.add_dependency(spir, 1)
Skill.all_skills.append(fars)

tele = Skill('TELE')
tele.add_dependency(gate, 1)
tele.add_dependency(fars, 2)
Skill.all_skills.append(tele)

port = Skill('PORT')
port.add_dependency(gate, 2)
port.add_dependency(fars, 1)
Skill.all_skills.append(port)

mind = Skill('MIND')
mind.add_dependency(patt, 1)
Skill.all_skills.append(mind)

weat = Skill('WEAT')
weat.add_dependency(patt, 1)
weat.add_dependency(forc, 1)
Skill.all_skills.append(weat)

swin = Skill('SWIN')
swin.add_dependency(weat, 1)
Skill.all_skills.append(swin)

ssto = Skill('SSTO')
ssto.add_dependency(weat, 1)
Skill.all_skills.append(ssto)

stor = Skill('STOR')
stor.add_dependency(weat, 3)
Skill.all_skills.append(stor)

call = Skill('CALL')
call.add_dependency(weat, 5)
Skill.all_skills.append(call)

clea = Skill('CLEA')
clea.add_dependency(weat, 1)
Skill.all_skills.append(clea)

eart = Skill('EART')
eart.add_dependency(patt, 1)
eart.add_dependency(forc, 1)
Skill.all_skills.append(eart)

wolf = Skill('WOLF')
wolf.add_dependency(eart, 1)
Skill.all_skills.append(wolf)

bird = Skill('BIRD')
bird.add_dependency(eart, 1)
Skill.all_skills.append(bird)

drag = Skill('DRAG')
drag.add_dependency(bird, 3)
drag.add_dependency(wolf, 3)
Skill.all_skills.append(drag)

necr = Skill('NECR')
necr.add_dependency(forc, 1)
necr.add_dependency(spir, 1)
Skill.all_skills.append(necr)

susk = Skill('SUSK')
susk.add_dependency(necr, 1)
Skill.all_skills.append(susk)

rais = Skill('RAIS')
rais.add_dependency(susk, 3)
Skill.all_skills.append(rais)

suli = Skill('SULI')
suli.add_dependency(rais, 3)
Skill.all_skills.append(suli)

fear = Skill('FEAR')
fear.add_dependency(necr, 1)
Skill.all_skills.append(fear)

sbla = Skill('SBLA')
sbla.add_dependency(necr, 5)
Skill.all_skills.append(sbla)

bund = Skill('BUND')
bund.add_dependency(necr, 1)
Skill.all_skills.append(bund)

demo = Skill('DEMO')
demo.add_dependency(spir, 1)
demo.add_dependency(forc, 1)
Skill.all_skills.append(demo)

suim = Skill('SUIM')
suim.add_dependency(demo, 1)
Skill.all_skills.append(suim)

sude = Skill('SUDE')
sude.add_dependency(suim, 3)
Skill.all_skills.append(sude)

suba = Skill('SUBA')
suba.add_dependency(sude, 3)
Skill.all_skills.append(suba)

bdem = Skill('BDEM')
bdem.add_dependency(demo, 1)
Skill.all_skills.append(bdem)

illu = Skill('ILLU')
illu.add_dependency(forc, 1)
illu.add_dependency(patt, 1)
Skill.all_skills.append(illu)

phen = Skill('PHEN')
phen.add_dependency(illu, 1)
Skill.all_skills.append(phen)

phbe = Skill('PHBE')
phen.add_dependency(illu, 1)
Skill.all_skills.append(phbe)

phde = Skill('PHDE')
phbe.add_dependency(illu, 1)
Skill.all_skills.append(phde)

invi = Skill('INVI')
invi.add_dependency(illu, 3)
Skill.all_skills.append(invi)

true = Skill('TRUE')
true.add_dependency(illu, 3)
Skill.all_skills.append(true)

disp = Skill('DISP')
disp.add_dependency(illu, 1)
Skill.all_skills.append(disp)

arti = Skill('ARTI')
arti.add_dependency(forc, 1)
arti.add_dependency(patt, 1)
arti.add_dependency(spir, 1)
Skill.all_skills.append(arti)
