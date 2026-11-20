"""
Inyector Seguro y Justificado para Pokémon Reloaded (The Last Beta 1.9.2.2)
==========================================================================
Diseñado para modificar legalmente y con 100% de integridad:
  * Dinero en cartera (con recalculo de vochodin, vsietedin y secodin)
  * Dinero en banco (con recalculo de vochoban, vsieteban y secoban)
  * Master Balls (con justificacion historica ev_1434 y ev_1435 para evadir chequeo de trampa)
  * Ultra Balls y Poke Balls (con recalculo de secovbl y vsietevbl)
  * Caramelos Raros, Vitaminas y Objetos (con recalculo de secovob y vsietevob)
  * Todos los 59 checkpoints criptograficos ACS recalculados y sincronizados.
  * Sincronizacion simultanea en reloaded1.savc y reloaded1_bk.savc.
  * 100% autonomo y portable (sin dependencias externas de descompilacion).
"""

import os, sys, re, shutil, time, subprocess, argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.join(BASE_DIR, "Proyecto Reloaded The Last Beta 1.9.2.2 Full")
if not os.path.exists(GAME_DIR) and os.path.exists(os.path.join(BASE_DIR, "data", "partidas")):
    GAME_DIR = BASE_DIR

SAVE_PATH = os.path.join(GAME_DIR, "data", "partidas", "reloaded1.savc")
SAVE_BK_PATH = os.path.join(GAME_DIR, "data", "partidas", "reloaded1_bk.savc")
RUN_LOADER_PATH = os.path.join(BASE_DIR, "run_loader.py")
if not os.path.exists(RUN_LOADER_PATH):
    RUN_LOADER_PATH = os.path.join(os.path.dirname(BASE_DIR), "run_loader.py")

BACKUP_DIR = os.path.join(BASE_DIR, "backups_inyector")

M_10010 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 36, 102, 98, 63, 80, 54, 121, 39, 78, 94, 118, 83, 37, 58, 93, 68, 96, 110, 42, 99, 32, 62, 105, 112, 90, 38, 84, 73, 61, 108, 69, 122, 65, 116, 95, 120, 87, 89, 107, 115, 74, 103, 44, 49, 67, 114, 52, 123, 47, 57, 82, 124, 33, 71, 79, 111, 91, 100, 119, 88, 117, 86, 106, 56, 41, 59, 43, 60, 48, 55, 51, 77, 53, 109, 75, 85, 46, 81, 34, 92, 40, 64, 126, 76, 70, 101, 66, 50, 45, 72, 104, 113, 125, 97, 35, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
M_10009 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 52, 84, 110, 126, 32, 44, 57, 39, 112, 96, 50, 98, 74, 120, 108, 80, 100, 75, 119, 102, 78, 104, 37, 101, 95, 81, 45, 97, 99, 60, 53, 35, 113, 64, 118, 76, 47, 62, 116, 85, 121, 59, 72, 106, 115, 103, 40, 86, 36, 109, 82, 43, 58, 107, 93, 68, 91, 69, 56, 88, 111, 46, 41, 66, 48, 125, 34, 51, 89, 117, 33, 73, 122, 54, 94, 70, 61, 105, 49, 87, 55, 123, 77, 71, 65, 92, 42, 90, 67, 38, 63, 79, 83, 124, 114, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
M_10008 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 35, 62, 66, 101, 84, 110, 43, 32, 86, 70, 46, 81, 34, 106, 71, 96, 68, 54, 122, 65, 39, 102, 59, 52, 74, 33, 80, 91, 103, 56, 95, 42, 99, 48, 69, 44, 77, 75, 57, 49, 90, 61, 120, 115, 97, 50, 112, 41, 117, 107, 82, 40, 38, 93, 85, 53, 73, 64, 45, 76, 47, 78, 58, 108, 123, 105, 121, 104, 116, 109, 113, 87, 111, 55, 89, 79, 118, 83, 37, 72, 124, 100, 126, 88, 94, 63, 98, 114, 119, 92, 60, 51, 125, 67, 36, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
M_10007 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 39, 57, 44, 32, 126, 110, 84, 52, 83, 79, 63, 38, 67, 90, 42, 92, 65, 71, 77, 123, 55, 87, 49, 105, 61, 70, 94, 54, 122, 73, 33, 117, 89, 51, 34, 125, 48, 66, 41, 46, 111, 88, 56, 69, 91, 68, 93, 107, 58, 43, 82, 109, 36, 86, 40, 103, 115, 106, 72, 59, 121, 85, 116, 62, 47, 76, 118, 64, 113, 35, 53, 60, 99, 97, 45, 81, 95, 101, 37, 104, 78, 102, 119, 75, 100, 80, 108, 120, 74, 98, 50, 96, 112, 124, 114, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]

m_10010 = {i: M_10010[i] for i in range(256)}
m_10009 = {i: M_10009[i] for i in range(256)}
m_10008 = {i: M_10008[i] for i in range(256)}
m_10007 = {i: M_10007[i] for i in range(256)}

def verify_save(savc_path):
    if not os.path.exists(savc_path):
        return False, f"No existe el archivo {savc_path}"
    data = open(savc_path, 'rb').read()
    pos = 0
    acs = 11
    checkpoints_verified = 0

    def ex_9342_v():
        nonlocal pos, acs
        assert data[pos] == 31; pos += 1
        ln = data[pos]; pos += 1
        if ln == 250:
            rlen = data[pos]; pos += 1
            s = "".join(chr(M_10010[data[pos+i]]) for i in range(rlen))
            pos += rlen
            acs += rlen
            return int(float(s))
        neg = False
        if ln >= 128:
            neg = True
            ln -= 128
        v = 0; mul = 1
        for i in range(ln):
            b = M_10010[data[pos]]; pos += 1
            v += b * mul
            mul *= 256
        if neg: v = -v
        acs += (abs(int(v)) % 241)
        return v

    def ex_9343_v():
        nonlocal pos, acs
        assert data[pos] == 31; pos += 1
        ln = data[pos] | (data[pos+1] << 8); pos += 2
        chars = []
        for i in range(1, ln + 1):
            b = M_10008[data[pos]]; pos += 1
            chars.append(chr(b))
            acs += (b * 7) + i
        return "".join(chars)

    def check_acs_v(seed):
        nonlocal pos, acs, checkpoints_verified
        assert data[pos] == 31; pos += 1
        stored = data[pos]; pos += 1
        calc = int(acs) % 251
        assert stored == calc, f"ACS checkpoint {checkpoints_verified} fallo! calc={calc}, stored={stored}"
        checkpoints_verified += 1
        acs = int(seed)
        return True

    def ex_v(fn, *args):
        if fn == 9342: return ex_9342_v()
        if fn == 9343: return ex_9343_v()
        if fn == 8141: return args[0] in (4, 5)
        return 0

    locs = {
        'ex': ex_v, 'check_acs': check_acs_v, 'ex_9343': ex_9343_v,
        'glb': DynamicState(), 'obj_3': DynamicState(), 'obj_18': DynamicState(),
        'obj_66': DynamicState(), 'obj_266': DynamicState(), 'obj_325': DynamicState(),
        'obj_331': DynamicState(), 'obj_518': DynamicState(), 'obj_1003': DynamicState(),
        'obj_1198': DynamicState(), 'obj_1330': DynamicState(), 'instance': DynamicState(),
    }
    code = open(RUN_LOADER_PATH, encoding='utf-8').read()
    code = code.replace('obj_3.vsietedin=ex(9343)', 'obj_3.vsietedin=ex_9343()')
    code = code.replace('obj_3.vsieteban=ex(9343)', 'obj_3.vsieteban=ex_9343()')
    exec(code, locs, locs)

    glb = locs['glb']
    obj_3 = locs['obj_3']
    obj_18 = locs['obj_18']
    mask1 = int(obj_3.mask1); mask2 = int(obj_3.mask2); mask3 = int(obj_3.mask3)

    if obj_3.colorbarra not in (0, 16994888):
        return False, f"Colorbarra error: {obj_3.colorbarra}"

    # Wallet
    vochodin = int(obj_3.vochodin); vsietedin = str(obj_3.vsietedin); secodin = int(obj_3.secodin)
    v8 = (((vochodin / 29) - (3 * mask3 + 15)) / 9)
    unidades = int(vsietedin[-1])
    sdin = int(vsietedin[-3:-1]) - 3 - (mask1 % 20)
    mon = (int(vsietedin[:-3]) - mask2 * 17) / 7
    if secodin > 70 or mon != glb.dinero or sdin != secodin:
        return False, "Wallet anti-cheat triggered"
    if (unidades % 2 == 1) and (mon - v8 >= 0): return False, "Wallet parity check 1 failed"
    if (unidades % 2 == 0) and (mon - v8 < 0): return False, "Wallet parity check 2 failed"

    # Bank
    vochoban = int(obj_3.vochoban); vsieteban = str(obj_3.vsieteban); secoban = int(obj_3.secoban)
    v8_ban = (((vochoban / 39) - (5 * mask1 + 23)) / 11)
    unidades_ban = int(vsieteban[-1])
    sban = int(vsieteban[-3:-1]) - 3 - (mask2 % 20)
    mon_ban = (int(vsieteban[:-3]) - mask3 * 47) / 6
    if secoban > 70 or mon_ban != obj_18.ingreso or sban != secoban:
        return False, "Bank anti-cheat triggered"
    if (unidades_ban % 2 == 1) and (mon_ban - v8_ban >= 0): return False, "Bank parity check 1 failed"
    if (unidades_ban % 2 == 0) and (mon_ban - v8_ban < 0): return False, "Bank parity check 2 failed"

    # Items
    secovob = int(obj_3.secovob)
    calc_vsietevob = (secovob + mask3) * 7
    for i in range(420):
        if int(glb.ObItem[i]) > 0 and int(glb.nObItem[i]) > 0:
            calc_vsietevob += (i * 23) + (int(glb.ObItem[i]) * 34) + (int(glb.nObItem[i]) * 21)
    if calc_vsietevob != int(obj_3.vsietevob):
        return False, f"Item bag anti-cheat mismatch: calc={calc_vsietevob}, stored={obj_3.vsietevob}"

    # Balls
    secovbl = int(obj_3.secovbl)
    calc_vsietevbl = (secovbl + mask1) * 8
    for i in range(30):
        if int(glb.ObBall[i]) > 0 and int(glb.nObBall[i]) > 0:
            calc_vsietevbl += (i * 7) + (int(glb.ObBall[i]) * 21) + (int(glb.nObBall[i]) * 39)
    if calc_vsietevbl != int(obj_3.vsietevbl):
        return False, f"Ball bag anti-cheat mismatch: calc={calc_vsietevbl}, stored={obj_3.vsietevbl}"

    # Master Ball
    has = 0
    for i in range(30):
        if int(glb.ObBall[i]) == 4: has += int(glb.nObBall[i])
    for i in range(1000):
        if int(glb.ObPC[i]) == 4: has += int(glb.nObPC[i])
    for i in range(6):
        if int(glb.objpoke1[i]) == 4: has += 1
    for c in range(1, int(glb.NumCajas) + 1):
        for j in range(30):
            if int(glb.boxobjpoke[c, j]) == 4: has += 1
    dis = int(obj_18.ev_1434) + 1 + int(obj_18.ev_1435) + 7
    if has > dis:
        return False, f"Master Ball check failed: has={has} > allowed={dis}"

    # PC Box Checksums
    for c in range(1, int(glb.NumCajas) + 1):
        v7_1 = 0
        for j in range(30):
            v7_1 += (j*2) + (int(glb.boxpkmn[c,j])*11) + (int(glb.boxnivel[c,j])*7) + int(glb.boxexp[c,j]) + 131
        v7_1 += (((int(obj_3.secocj[c]) + mask3) * 43) + ((29 + mask2) * 3 * c))
        if v7_1 != int(obj_3.vsietecj[c]):
            return False, f"Caja {c} vsietecj mismatch!"

        v7_2 = 0
        for j in range(30):
            v7_2 += (j*2) + (int(glb.boxIV[c,j])*13) + 41
            v7_2 += (j*4) + (int(glb.boxobjpoke[c,j])*23) + 41
            v7_2 += (j*3) + (int(glb.boxpkmnsex[c,j])*15) + 41
            v7_2 += (j*5) + (int(glb.boxselue_pk[c,j])*16) + 41
            v7_2 += (j*7) + (int(glb.boxat1[c,j])*11) + 41
            v7_2 += (j*9) + (int(glb.boxat2[c,j])*12) + 41
            v7_2 += (j*6) + (int(glb.boxat3[c,j])*19) + 41
            v7_2 += (j*8) + (int(glb.boxat4[c,j])*14) + 41
        v7_2 += (((int(obj_3.secocj2[c]) + mask2) * 23) + ((19 + mask1) * 2 * c))
        if v7_2 != int(obj_3.vsietecj2[c]):
            return False, f"Caja {c} vsietecj2 mismatch!"

    # MTs Bag
    secovmt = int(obj_3.secovmt)
    calc_vsietevmt = (secovmt + mask2) * 13
    for i in range(1000):
        if int(glb.ObMT[i]) > 0 and int(glb.nObMT[i]) > 0:
            calc_vsietevmt += (i * 13) + (int(glb.ObMT[i]) * 43) + (int(glb.nObMT[i]) * 26)
    if calc_vsietevmt != int(obj_3.vsietevmt):
        return False, f"MT bag anti-cheat mismatch: calc={calc_vsietevmt}, stored={obj_3.vsietevmt}"

    # Party Pokemon Checksums (vsietepk and vsietepk2 / Anomaly 8315692)
    calc_pk = (((int(obj_3.secopk) + mask1) * 7) + ((15 + mask2) * 6))
    for i in range(6):
        calc_pk += (i*7) + (int(glb.pkmn1[i])*14) + (int(glb.nivel1[i])*11) + int(glb.exp1[i]) + 361
        calc_pk += (i*3) + (int(glb.pkmn2[i])*11) + (int(glb.nivel2[i])*14) + int(glb.exp2[i]) + 135
    if calc_pk != int(obj_3.vsietepk):
        return False, f"Party pkmn checksum mismatch (vsietepk): calc={calc_pk}, stored={obj_3.vsietepk}"

    calc_pk2 = (((int(obj_3.secopk2) + mask1) * 7) + ((15 + mask2) * 6))
    for i in range(6):
        calc_pk2 += (i*7) + (int(glb.PP_1[i])*6) + (int(glb.PS_1[i])*7) + int(glb.STD1[i]) + 361
        calc_pk2 += (i*3) + (int(glb.IV[i])*7) + (int(glb.objpoke1[i])*6) + (int(glb.selue_pk1[i])*11) + int(glb.pkmnsex1[i]) + 361
        calc_pk2 += (i*7) + (int(glb.PP_2[i])*6) + (int(glb.PS_2[i])*7) + int(glb.STD2[i]) + 361
        calc_pk2 += (i*3) + (int(glb.IV2[i])*7) + (int(glb.objpoke2[i])*6) + (int(glb.selue_pk2[i])*11) + int(glb.pkmnsex2[i]) + 361
        for j in range(1, 5):
            calc_pk2 += int(glb.attack1[i, j]) * 7 * j
            calc_pk2 += int(glb.attack2[i, j]) * 7 * j
        v1 = round(glb.vel1[i] * 100)
        v2 = round(glb.vel2[i] * 100)
        calc_pk2 += (i*13) + (((int(glb.actual1)+8)*5) + (int(glb.MAX_PP_1[i])*2) + (int(glb.MAX_PS_1[i])*2) + (int(glb.XTRA_PS_1[i])*2) + (int(glb.atk1[i])*3) + (int(glb.def1[i])*3) + (v1 * 7))
        calc_pk2 += (int(glb.atk_sp1[i])*5) + (int(glb.def_sp1[i])*3) + (int(glb.prec1[i])*4) + (int(glb.tipoA1[i])*6) + (int(glb.tipoB1[i])*5) + (int(glb.tipoC1[i])*4)
        calc_pk2 += (i*13) + (((int(glb.actual2)+8)*5) + (int(glb.MAX_PP_2[i])*2) + (int(glb.MAX_PS_2[i])*2) + (int(glb.XTRA_PS_2[i])*2) + (int(glb.atk2[i])*3) + (int(glb.def2[i])*3) + (v2 * 9))
        calc_pk2 += (int(glb.atk_sp2[i])*5) + (int(glb.def_sp2[i])*3) + (int(glb.prec2[i])*4) + (int(glb.tipoA2[i])*6) + (int(glb.tipoB2[i])*5) + (int(glb.tipoC2[i])*4)
    calc_pk2 = int(calc_pk2) % 1000000
    if calc_pk2 != int(obj_3.vsietepk2):
        return False, f"Party pkmn battle checksum mismatch (vsietepk2 / Anomaly 8315692): calc={calc_pk2}, stored={obj_3.vsietepk2}"

    return True, f"Todos los {checkpoints_verified} checkpoints criptograficos y checksums verificados al 100%"

def encode_num(val):
    out = [31]
    val = int(val)
    if abs(val) > 2147483647:
        out.append(250)
        s = str(val)
        out.append(len(s))
        for ch in s:
            out.append(m_10009[ord(ch)])
        return bytes(out), len(s)
    neg = False
    v = val
    if v < 0:
        neg = True
        v = abs(v)
    temp = v
    length = 1
    while temp >= 256:
        temp = temp // 256
        length += 1
    ln_byte = length + 128 if neg else length
    out.append(ln_byte)
    curr = v
    for _ in range(length):
        out.append(m_10009[curr % 256])
        curr = curr // 256
    return bytes(out), abs(val) % 241

def encode_str(s):
    out = [31]
    ln = len(s)
    out.append(ln & 255)
    out.append((ln >> 8) & 255)
    acs_contrib = 0
    for idx, ch in enumerate(s, start=1):
        byte_val = ord(ch)
        out.append(m_10007[byte_val])
        acs_contrib += (byte_val * 7) + idx
    return bytes(out), acs_contrib

class DynamicState:
    def __init__(self): self._d = {}
    def __getattr__(self, name):
        if name.startswith('_'): return super().__getattr__(name)
        if name not in self._d: self._d[name] = DynamicState()
        return self._d[name]
    def __setattr__(self, name, val):
        if name.startswith('_'): super().__setattr__(name, val)
        else: self._d[name] = val
    def __getitem__(self, idx):
        if idx not in self._d: self._d[idx] = DynamicState()
        return self._d[idx]
    def __setitem__(self, idx, val): self._d[idx] = val

def check_game_process():
    cmd = 'Get-Process -Name "*reloaded*", "*Pokemon*" -ErrorAction SilentlyContinue'
    r = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    if r.stdout.strip():
        print("[ADVERTENCIA] Pokémon Reloaded parece estar en ejecución.")
        print("Por favor cierra el juego antes de inyectar para evitar conflictos.")
        return False
    return True

def load_save_state(savc_data):
    pos = 0
    acs = 11
    
    def ex_9342_read():
        nonlocal pos, acs
        assert savc_data[pos] == 31; pos += 1
        ln = savc_data[pos]; pos += 1
        if ln == 250:
            rlen = savc_data[pos]; pos += 1
            s = "".join(chr(m_10010[savc_data[pos+i]]) for i in range(rlen))
            pos += rlen
            acs += rlen
            return int(float(s))
        neg = False
        if ln >= 128:
            neg = True
            ln -= 128
        v = 0; mul = 1
        for i in range(ln):
            b = m_10010[savc_data[pos]]; pos += 1
            v += b * mul
            mul *= 256
        if neg: v = -v
        acs += (abs(int(v)) % 241)
        return v

    def ex_9343_read():
        nonlocal pos, acs
        assert savc_data[pos] == 31; pos += 1
        ln = savc_data[pos] | (savc_data[pos+1] << 8); pos += 2
        chars = []
        for i in range(1, ln + 1):
            b = m_10008[savc_data[pos]]; pos += 1
            chars.append(chr(b))
            acs += (b * 7) + i
        return "".join(chars)

    def check_acs_read(seed):
        nonlocal pos, acs
        assert savc_data[pos] == 31; pos += 1
        pos += 1
        acs = int(seed)
        return True

    def ex_read(fn, *args):
        if fn == 9342: return ex_9342_read()
        if fn == 9343: return ex_9343_read()
        if fn == 8141: return args[0] in (4, 5)
        return 0

    locs = {
        'ex': ex_read, 'check_acs': check_acs_read, 'ex_9343': ex_9343_read,
        'glb': DynamicState(), 'obj_3': DynamicState(), 'obj_18': DynamicState(),
        'obj_66': DynamicState(), 'obj_266': DynamicState(), 'obj_325': DynamicState(),
        'obj_331': DynamicState(), 'obj_518': DynamicState(), 'obj_1003': DynamicState(),
        'obj_1198': DynamicState(), 'obj_1330': DynamicState(), 'instance': DynamicState(),
    }
    
    code = open(RUN_LOADER_PATH, encoding="utf-8").read()
    code = code.replace("obj_3.vsietedin=ex(9343)", "obj_3.vsietedin=ex_9343()")
    code = code.replace("obj_3.vsieteban=ex(9343)", "obj_3.vsieteban=ex_9343()")
    exec(code, locs, locs)
    return locs

SHOP_CASINO_MTS = [
    (5076, "MT15 Hiperrayo (Casino)"),
    (5016, "MT17 Terremoto (Casino)"),
    (5040, "MT25 Rayo (Casino)"),
    (5072, "MT27 Rayo Hielo (Casino)"),
    (5001, "MT31 Lanzallamas (Casino)"),
    (5208, "MT10 Día Soleado (Centro Comercial)"),
    (5207, "MT11 Danza Lluvia (Centro Comercial)"),
    (5210, "MT12 Granizo (Centro Comercial)"),
    (5106, "MT14 Doble Equipo (Centro Comercial)"),
    (5203, "MT18 Protección (Centro Comercial)"),
    (5418, "MT20 Onda Certera (Centro Comercial)"),
    (5093, "MT24 Onda Trueno (Centro Comercial)"),
    (5251, "MT33 Gigadrenado (Centro Comercial)"),
    (5345, "MT35 Tumbarocas (Centro Comercial)"),
    (5217, "MT38 Puya Nociva (Centro Comercial)"),
    (5030, "MT55 Puño Trueno (Centro Comercial)"),
    (5028, "MT56 Puño Fuego (Centro Comercial)"),
    (5029, "MT57 Puño Hielo (Centro Comercial)"),
    (5117, "MT73 Reflejo (Centro Comercial)")
]

BALL_IDS = set(range(1, 14)) | set(range(472, 484)) | {522}
KEY_ITEM_IDS = {14, 484, 568, 658, 674, 679} | set(range(152, 194)) | set(range(607, 618))

def _decode_game_text(raw):
    res = "".join(chr(M_10010[ord(c)]) for c in raw)
    for k, v in (
        ("&{a}", "á"), ("&{e}", "é"), ("&{i}", "í"), ("&{o}", "ó"), ("&{u}", "ú"), ("&{n}", "ñ"),
        ("&{A}", "Á"), ("&{E}", "É"), ("&{I}", "Í"), ("&{O}", "Ó"), ("&{U}", "Ú"), ("&{N}", "Ñ"),
        ("&{!}", "¡"), ("&{?}", "¿"),
    ):
        res = res.replace(k, v)
    return res.strip()

def _load_desc_lines():
    desc_path = os.path.join(GAME_DIR, "data", "text", "es", "txt_obj_desc.dll")
    if not os.path.exists(desc_path):
        desc_path = os.path.join(GAME_DIR, "data", "text", "en", "txt_obj_desc.dll")
    if not os.path.exists(desc_path):
        return []
    with open(desc_path, "r", encoding="latin-1") as f:
        return [_decode_game_text(l.rstrip("\r\n")) for l in f]

def _get_item_description(idx, name, desc_lines):
    raw = ""
    if desc_lines:
        if 1 <= idx <= 90 and idx - 1 < len(desc_lines):
            raw = desc_lines[idx - 1]
        elif 91 <= idx <= 107 and 90 < len(desc_lines):
            raw = desc_lines[90].replace("$par1$", name.replace("Tabla ", "tipo "))
        elif idx == 108 and 91 < len(desc_lines):
            raw = desc_lines[91]
        elif 109 <= idx <= 193 and idx - 17 < len(desc_lines):
            raw = desc_lines[idx - 17]
        elif 291 <= idx <= 383 and idx - 114 < len(desc_lines):
            raw = desc_lines[idx - 114]
        elif 384 <= idx <= 400 and 270 < len(desc_lines):
            raw = desc_lines[270].replace("$par1$", name.replace("Gema ", ""))
        elif 401 <= idx <= 471 and idx - 129 < len(desc_lines):
            raw = desc_lines[idx - 129]
        elif 472 <= idx <= 483 and idx - 128 < len(desc_lines):
            raw = desc_lines[idx - 128]
        elif 638 <= idx <= 821 and idx + 939 < len(desc_lines):
            cand = desc_lines[idx + 939]
            if not cand.startswith(f"{idx} "):
                raw = cand

    if raw:
        return raw.replace("$par1$", "la tecla asignada")

    if name.startswith("MT") or name.startswith("MO"):
        kind = "Máquina Oculta" if name.startswith("MO") else "Máquina Técnica"
        move = name.split(" ", 1)[1] if " " in name else name
        return f"{kind}: enseña el movimiento {move}."
    if "stal Z" in name:
        return "Cristal Z: permite ejecutar el movimiento Z correspondiente en combate."
    if name.startswith("Teralito "):
        return f"Cambia el Teratipo de un Pokémon a {name.replace('Teralito ', '')}."
    if name.startswith("Mochi "):
        return "Modifica o reinicia los puntos de esfuerzo (EVs) de un Pokémon."
    if name.startswith("Incienso "):
        return "Objeto equipable que potencia movimientos o habilita cría especial."
    if any(name.endswith(sfx) for sfx in ("ita", "ita X", "ita Y", "ita Z")):
        return "Megapiedra: permite megaevolucionar en combate al Pokémon correspondiente."
    if name == "Ente Ball":
        return "Poké Ball especial diseñada para capturar Ultraentes."
    return "Objeto especial del juego."

def load_item_catalog():
    """Carga el catálogo de objetos y Poké Balls seguros desde txt_obj.dll."""
    txt_path = os.path.join(GAME_DIR, "data", "text", "es", "txt_obj.dll")
    if not os.path.exists(txt_path):
        txt_path = os.path.join(GAME_DIR, "data", "text", "en", "txt_obj.dll")
    if not os.path.exists(txt_path):
        return []

    desc_lines = _load_desc_lines()
    catalog = []
    with open(txt_path, "r", encoding="latin-1") as f:
        for idx, line in enumerate(f, start=1):
            name = _decode_game_text(line.rstrip("\r\n"))
            if not name or name in ("---", "???"):
                continue
            if idx in BALL_IDS:
                catalog.append({"id": idx, "name": name, "pocket": "ball", "desc": _get_item_description(idx, name, desc_lines)})
            elif idx in KEY_ITEM_IDS:
                continue
            elif name.startswith("Baya ") or name.startswith("MT") or name.startswith("MO"):
                continue
            else:
                catalog.append({"id": idx, "name": name, "pocket": "item", "desc": _get_item_description(idx, name, desc_lines)})
    return catalog

def load_mt_catalog():
    """Carga el catálogo completo de MTs y MOs oficiales desde txt_obj.dll."""
    txt_path = os.path.join(GAME_DIR, "data", "text", "es", "txt_obj.dll")
    if not os.path.exists(txt_path):
        txt_path = os.path.join(GAME_DIR, "data", "text", "en", "txt_obj.dll")
    if not os.path.exists(txt_path):
        return []

    desc_lines = _load_desc_lines()
    mts = []
    with open(txt_path, "r", encoding="latin-1") as f:
        for idx, line in enumerate(f, start=1):
            name = _decode_game_text(line.rstrip("\r\n"))
            if name.startswith("MT") or name.startswith("MO"):
                mts.append({"id": idx, "name": name, "pocket": "mt", "desc": _get_item_description(idx, name, desc_lines)})
    return mts

def load_pokemon_catalog():
    """Carga el catálogo completo de Pokémon desde txt_pkmn.dll."""
    txt_path = os.path.join(GAME_DIR, "data", "text", "es", "txt_pkmn.dll")
    if not os.path.exists(txt_path):
        txt_path = os.path.join(GAME_DIR, "data", "text", "en", "txt_pkmn.dll")
    if not os.path.exists(txt_path):
        return []
    res = []
    with open(txt_path, "r", encoding="latin-1") as f:
        for idx, line in enumerate(f, start=1):
            name = _decode_game_text(line.rstrip("\r\n"))
            if name and name != "-" and not name.startswith("?"):
                res.append({"id": idx, "name": name})
    return res

def load_attack_catalog():
    """Carga el catálogo completo de ataques/movimientos desde txt_attack.dll."""
    txt_path = os.path.join(GAME_DIR, "data", "text", "es", "txt_attack.dll")
    if not os.path.exists(txt_path):
        txt_path = os.path.join(GAME_DIR, "data", "text", "en", "txt_attack.dll")
    if not os.path.exists(txt_path):
        return []
    res = []
    with open(txt_path, "r", encoding="latin-1") as f:
        for idx, line in enumerate(f, start=1):
            name = _decode_game_text(line.rstrip("\r\n"))
            if name and name != "-":
                res.append({"id": idx, "name": name})
    return res

# 3 Equipos TOP de Aventura para Pokémon Reloaded (todos Nv.42, IVs 999999, Restos)
TOP_ADVENTURE_TEAMS = {
    "equilibrado": [
        {"pkmn_id": 445, "name": "Garchomp",   "level": 42, "iv": 999999, "attacks": [17, 197, 446, 212], "item_id": 303, "sex": 1},
        {"pkmn_id": 282, "name": "Gardevoir",  "level": 42, "iv": 999999, "attacks": [43, 566, 41, 16],   "item_id": 303, "sex": 2},
        {"pkmn_id": 753, "name": "Greninja",   "level": 42, "iv": 999999, "attacks": [9, 73, 411, 578],   "item_id": 303, "sex": 1},
        {"pkmn_id": 758, "name": "Talonflame", "level": 42, "iv": 999999, "attacks": [202, 421, 2, 377],  "item_id": 303, "sex": 1},
        {"pkmn_id": 376, "name": "Metagross",  "level": 42, "iv": 999999, "attacks": [338, 432, 30, 17],  "item_id": 303, "sex": 0},
        {"pkmn_id": 254, "name": "Sceptile",   "level": 42, "iv": 999999, "attacks": [372, 252, 414, 419],"item_id": 303, "sex": 1},
    ],
    "ofensivo": [
        {"pkmn_id": 6,   "name": "Charizard",  "level": 42, "iv": 999999, "attacks": [2, 199, 414, 40],   "item_id": 303, "sex": 1},
        {"pkmn_id": 448, "name": "Lucario",    "level": 42, "iv": 999999, "attacks": [409, 338, 282, 17], "item_id": 303, "sex": 1},
        {"pkmn_id": 94,  "name": "Gengar",     "level": 42, "iv": 999999, "attacks": [16, 239, 41, 419],  "item_id": 303, "sex": 1},
        {"pkmn_id": 149, "name": "Dragonite",  "level": 42, "iv": 999999, "attacks": [197, 282, 29, 17],  "item_id": 303, "sex": 1},
        {"pkmn_id": 260, "name": "Swampert",   "level": 42, "iv": 999999, "attacks": [129, 17, 30, 159],  "item_id": 303, "sex": 1},
        {"pkmn_id": 135, "name": "Jolteon",    "level": 42, "iv": 999999, "attacks": [41, 16, 505, 94],   "item_id": 303, "sex": 1},
    ],
    "tanques": [
        {"pkmn_id": 248, "name": "Tyranitar",  "level": 42, "iv": 999999, "attacks": [446, 212, 17, 30],  "item_id": 303, "sex": 1},
        {"pkmn_id": 257, "name": "Blaziken",   "level": 42, "iv": 999999, "attacks": [330, 390, 159, 421],"item_id": 303, "sex": 1},
        {"pkmn_id": 130, "name": "Gyarados",   "level": 42, "iv": 999999, "attacks": [129, 373, 17, 212], "item_id": 303, "sex": 1},
        {"pkmn_id": 3,   "name": "Venusaur",   "level": 42, "iv": 999999, "attacks": [252, 239, 91, 87],  "item_id": 303, "sex": 1},
        {"pkmn_id": 65,  "name": "Alakazam",   "level": 42, "iv": 999999, "attacks": [43, 16, 419, 568],  "item_id": 303, "sex": 1},
        {"pkmn_id": 212, "name": "Scizor",     "level": 42, "iv": 999999, "attacks": [426, 413, 312, 377],"item_id": 303, "sex": 1},
    ],
}

ADVENTURE_DREAM_TEAM = TOP_ADVENTURE_TEAMS["equilibrado"]

# 18 Pokémon Únicos / Exclusivos 100% Seguros de Pokémon Reloaded (sin bloqueo de historia ex(6970))
# Nota: Latly (499), Mewthree (500), Psicovenom (516) y Gripherial (517) requieren flags de postgame en LoaderControl (J30/J31/J53/J54).
RELOADED_EXCLUSIVES = [
    {"pkmn_id": 504, "name": "Orphegasus",      "level": 42, "iv": 999999, "attacks": [202, 421, 2, 40],   "item_id": 303, "sex": 1},
    {"pkmn_id": 511, "name": "Torkore",         "level": 42, "iv": 999999, "attacks": [2, 202, 17, 446],   "item_id": 303, "sex": 1},
    {"pkmn_id": 509, "name": "Rekivolt",        "level": 42, "iv": 999999, "attacks": [41, 446, 505, 17],  "item_id": 303, "sex": 1},
    {"pkmn_id": 514, "name": "Harfetch'd",      "level": 42, "iv": 999999, "attacks": [421, 372, 390, 377],"item_id": 303, "sex": 1},
    {"pkmn_id": 506, "name": "Phanteon",        "level": 42, "iv": 999999, "attacks": [16, 411, 43, 419],  "item_id": 303, "sex": 1},
    {"pkmn_id": 515, "name": "Chartfortt",      "level": 42, "iv": 999999, "attacks": [199, 43, 41, 377],  "item_id": 303, "sex": 1},
    {"pkmn_id": 513, "name": "Betearow",        "level": 42, "iv": 999999, "attacks": [421, 199, 40, 377], "item_id": 303, "sex": 1},
    {"pkmn_id": 497, "name": "Pryncice",        "level": 42, "iv": 999999, "attacks": [73, 43, 16, 419],   "item_id": 303, "sex": 2},
    {"pkmn_id": 508, "name": "Rockeon",         "level": 42, "iv": 999999, "attacks": [446, 17, 159, 212], "item_id": 303, "sex": 1},
    {"pkmn_id": 507, "name": "Drakeon",         "level": 42, "iv": 999999, "attacks": [414, 197, 2, 17],   "item_id": 303, "sex": 1},
    {"pkmn_id": 505, "name": "Eeveon",          "level": 42, "iv": 999999, "attacks": [282, 16, 17, 377],  "item_id": 303, "sex": 1},
    {"pkmn_id": 498, "name": "Onix de Cristal", "level": 42, "iv": 999999, "attacks": [17, 446, 73, 212],  "item_id": 303, "sex": 1},
    {"pkmn_id": 512, "name": "Scyclaw",         "level": 42, "iv": 999999, "attacks": [413, 421, 312, 377],"item_id": 303, "sex": 1},
    {"pkmn_id": 495, "name": "Pikablue",        "level": 42, "iv": 999999, "attacks": [41, 9, 73, 505],    "item_id": 303, "sex": 1},
    {"pkmn_id": 496, "name": "Ghost",           "level": 42, "iv": 999999, "attacks": [16, 43, 411, 41],   "item_id": 303, "sex": 0},
    {"pkmn_id": 503, "name": "Kytto",           "level": 42, "iv": 999999, "attacks": [16, 411, 41, 43],   "item_id": 303, "sex": 2},
    {"pkmn_id": 494, "name": "Terodactyl",      "level": 42, "iv": 999999, "attacks": [446, 17, 197, 40],  "item_id": 303, "sex": 1},
    {"pkmn_id": 510, "name": "Tursoot",         "level": 42, "iv": 999999, "attacks": [2, 17, 159, 239],   "item_id": 303, "sex": 1},
]

def execute_injection(dinero=None, banco=None, masterballs=None, ultraballs=None, caramelos=None, vitaminas=None, items_custom=None, balls_custom=None, mts=None, box_pokemon=None, max_party_stats=False):
    if not check_game_process():
        raise RuntimeError("Pokémon Reloaded está en ejecución. Ciérralo antes de inyectar.")
        
    if not os.path.exists(SAVE_PATH):
        raise FileNotFoundError(f"No se encuentra el archivo de partida en {SAVE_PATH}")
        
    orig_data = open(SAVE_PATH, 'rb').read()
    
    # 1. Crear backup automático
    ts = time.strftime("%Y%m%d_%H%M%S")
    b_dir = os.path.join(BACKUP_DIR, f"injector_{ts}")
    os.makedirs(b_dir, exist_ok=True)
    shutil.copy2(SAVE_PATH, os.path.join(b_dir, "reloaded1.savc"))
    if os.path.exists(SAVE_BK_PATH):
        shutil.copy2(SAVE_BK_PATH, os.path.join(b_dir, "reloaded1_bk.savc"))
    print(f"[*] Respaldo de seguridad creado en: {b_dir}")
    
    # 2. Leer estado actual
    state = load_save_state(orig_data)
    glb = state['glb']
    obj_3 = state['obj_3']
    obj_18 = state['obj_18']
    
    mask1 = int(obj_3.mask1)
    mask2 = int(obj_3.mask2)
    mask3 = int(obj_3.mask3)
    
    replacements = {}
    
    # A. Dinero en cartera
    if dinero is not None:
        target_dinero = int(dinero)
        replacements['glb.dinero'] = target_dinero
        old_din = 10000
        vochodin = ((old_din * 9) + (3 * mask3 + 15)) * 29
        secodin = 25
        sdin_str = f"{secodin + 3 + (mask1 % 20):02d}"
        mon_str = str(target_dinero * 7 + mask2 * 17)
        # unidades par (4) si target_dinero >= old_din
        vsietedin = f"{mon_str}{sdin_str}4" if target_dinero >= old_din else f"{mon_str}{sdin_str}1"
        replacements['obj_3.secodin'] = secodin
        replacements['obj_3.vsietedin'] = vsietedin
        replacements['obj_3.vochodin'] = vochodin
        print(f"[+] Dinero en cartera: {glb.dinero} € -> {target_dinero} € (vsietedin={vsietedin})")

    # B. Dinero en banco
    if banco is not None:
        target_banco = int(banco)
        replacements['obj_18.ingreso'] = target_banco
        replacements['obj_18.cuentacorriente'] = 1
        old_ban = 10000
        vochoban = ((old_ban * 11) + (5 * mask1 + 23)) * 39
        secoban = 15
        sban_str = f"{secoban + 3 + (mask2 % 20):02d}"
        mon_ban_str = str(target_banco * 6 + mask3 * 47)
        vsieteban = f"{mon_ban_str}{sban_str}4" if target_banco >= old_ban else f"{mon_ban_str}{sban_str}1"
        replacements['obj_3.secoban'] = secoban
        replacements['obj_3.vsieteban'] = vsieteban
        replacements['obj_3.vochoban'] = vochoban
        print(f"[+] Dinero en banco: {obj_18.ingreso} € -> {target_banco} € (vsieteban={vsieteban})")

    def _set_pocket_slot(arr, narr, prefix, capacity, item_id, count):
        count = max(0, int(count))
        for i in range(capacity):
            if int(arr[i]) == item_id:
                if count == 0:
                    arr[i] = 0
                    narr[i] = 0
                    replacements[f'{prefix}[{i}]'] = 0
                    replacements[f'glb.n{prefix[4:]}[{i}]'] = 0
                else:
                    narr[i] = count
                    replacements[f'glb.n{prefix[4:]}[{i}]'] = count
                return True
        if count == 0:
            return False
        for i in range(capacity):
            if int(arr[i]) == 0:
                arr[i] = item_id
                narr[i] = count
                replacements[f'{prefix}[{i}]'] = item_id
                replacements[f'glb.n{prefix[4:]}[{i}]'] = count
                return True
        raise RuntimeError(f"La mochila ({prefix}) está llena (máximo {capacity} espacios).")

    def _justify_masterballs():
        has = 0
        for i in range(30):
            if int(glb.ObBall[i]) == 4: has += int(glb.nObBall[i])
        for i in range(1000):
            if int(glb.ObPC[i]) == 4: has += int(glb.nObPC[i])
        for i in range(6):
            if int(glb.objpoke1[i]) == 4: has += 1
        for c in range(1, int(glb.NumCajas) + 1):
            for j in range(30):
                if int(glb.boxobjpoke[c, j]) == 4: has += 1
        ev_1435 = int(obj_18.ev_1435) if int(obj_18.ev_1435) > 0 else 1
        req_ev1434 = max(1, has - ev_1435 - 8 + 2)
        replacements['obj_18.ev_1434'] = req_ev1434
        print(f"    [*] Justificación legal de Master Ball calibrada: ev_1434={req_ev1434} (Total={has}, Límite={req_ev1434 + 1 + ev_1435 + 7})")

    # C. Mochila de Balls
    ball_changes = False

    def set_ball(ball_id, count):
        nonlocal ball_changes
        _set_pocket_slot(glb.ObBall, glb.nObBall, 'glb.ObBall', 30, ball_id, count)
        ball_changes = True

    if masterballs is not None:
        target_mb = int(masterballs)
        set_ball(4, target_mb)
        print(f"[+] Master Balls: {target_mb} unidades")
        _justify_masterballs()

    if ultraballs is not None:
        target_ub = int(ultraballs)
        set_ball(3, target_ub)
        print(f"[+] Ultra Balls: {target_ub} unidades")

    if balls_custom:
        for b_id, b_count in balls_custom:
            b_id = int(b_id)
            b_count = int(b_count)
            set_ball(b_id, b_count)
            print(f"[+] Ball personalizada (ID {b_id}): {b_count} unidades")
            if b_id == 4:
                _justify_masterballs()

    if ball_changes:
        secovbl = int(obj_3.secovbl)
        calc_vsietevbl = (secovbl + mask1) * 8
        for i in range(30):
            b_id = int(glb.ObBall[i])
            b_n = int(glb.nObBall[i])
            if b_id > 0 and b_n > 0:
                calc_vsietevbl += (i * 7) + (b_id * 21) + (b_n * 39)
        replacements['obj_3.vsietevbl'] = calc_vsietevbl
        print(f"    [*] Checksum de Balls recalculado: vsietevbl={calc_vsietevbl}")

    # D. Mochila de Objetos
    item_changes = False

    def set_item(item_id, count):
        nonlocal item_changes
        _set_pocket_slot(glb.ObItem, glb.nObItem, 'glb.ObItem', 420, item_id, count)
        item_changes = True

    if caramelos is not None:
        target_car = int(caramelos)
        set_item(38, target_car)
        print(f"[+] Caramelos Raros: {target_car} unidades")

    if vitaminas is not None:
        v_count = int(vitaminas)
        for vit_id, vit_name in [(32, 'Más PS'), (33, 'Calcio'), (34, 'Hierro'), (35, 'Carbohidratos'), (36, 'Proteína'), (37, 'Zinc')]:
            set_item(vit_id, v_count)
            print(f"[+] Vitamina {vit_name} (ID {vit_id}): {v_count} unidades")

    if items_custom:
        for it_id, it_count in items_custom:
            it_id = int(it_id)
            it_count = int(it_count)
            if it_id in BALL_IDS:
                set_ball(it_id, it_count)
                print(f"[+] Ball personalizada (ID {it_id}): {it_count} unidades")
                if it_id == 4:
                    _justify_masterballs()
            elif it_id in KEY_ITEM_IDS:
                raise ValueError(f"El objeto ID {it_id} es un Objeto Clave y no se puede inyectar en la mochila normal.")
            else:
                set_item(it_id, it_count)
                print(f"[+] Objeto personalizado (ID {it_id}): {it_count} unidades")

    if ball_changes:
        secovbl = int(obj_3.secovbl)
        calc_vsietevbl = (secovbl + mask1) * 8
        for i in range(30):
            b_id = int(glb.ObBall[i])
            b_n = int(glb.nObBall[i])
            if b_id > 0 and b_n > 0:
                calc_vsietevbl += (i * 7) + (b_id * 21) + (b_n * 39)
        replacements['obj_3.vsietevbl'] = calc_vsietevbl
        print(f"    [*] Checksum de Balls recalculado: vsietevbl={calc_vsietevbl}")

    if item_changes:
        secovob = int(obj_3.secovob)
        calc_vsietevob = (secovob + mask3) * 7
        for i in range(420):
            it_id = int(glb.ObItem[i])
            it_n = int(glb.nObItem[i])
            if it_id > 0 and it_n > 0:
                calc_vsietevob += (i * 23) + (it_id * 34) + (it_n * 21)
        replacements['obj_3.vsietevob'] = calc_vsietevob
        print(f"    [*] Checksum de Objetos recalculado: vsietevob={calc_vsietevob}")

    # E. Mochila de MTs
    mt_changes = False
    if mts is not None:
        mt_list_to_inject = []
        if mts is True:
            mt_list_to_inject = [(mid, 1) for mid, _name in SHOP_CASINO_MTS]
        elif mts == "all":
            mt_list_to_inject = [(m["id"], 1) for m in load_mt_catalog() if m["name"].startswith("MT")]
        elif isinstance(mts, (list, tuple)):
            for item in mts:
                if isinstance(item, (list, tuple)):
                    mt_list_to_inject.append((int(item[0]), max(0, int(item[1]))))
                else:
                    mt_list_to_inject.append((int(item), 1))

        mt_slots = {}
        for i in range(1000):
            mid = int(glb.ObMT[i])
            qty = int(glb.nObMT[i])
            if mid > 0 and qty > 0:
                mt_slots[i] = (mid, qty)

        next_slot = max(mt_slots.keys(), default=-1) + 1
        for mt_id, target_qty in mt_list_to_inject:
            found_slot = None
            for slot_idx, (mid, _q) in mt_slots.items():
                if mid == mt_id:
                    found_slot = slot_idx
                    break
            if found_slot is not None:
                if target_qty == 0:
                    mt_slots.pop(found_slot, None)
                    replacements[f'glb.ObMT[{found_slot}]'] = 0
                    replacements[f'glb.nObMT[{found_slot}]'] = 0
                    glb.ObMT[found_slot] = 0
                    glb.nObMT[found_slot] = 0
                    mt_changes = True
                elif mt_slots[found_slot][1] != target_qty:
                    mt_slots[found_slot] = (mt_id, target_qty)
                    replacements[f'glb.nObMT[{found_slot}]'] = target_qty
                    glb.nObMT[found_slot] = target_qty
                    mt_changes = True
            elif target_qty > 0:
                if next_slot >= 1000:
                    raise RuntimeError("La mochila de MTs está llena (máximo 1000 espacios).")
                mt_slots[next_slot] = (mt_id, target_qty)
                replacements[f'glb.ObMT[{next_slot}]'] = mt_id
                replacements[f'glb.nObMT[{next_slot}]'] = target_qty
                glb.ObMT[next_slot] = mt_id
                glb.nObMT[next_slot] = target_qty
                next_slot += 1
                mt_changes = True
                
        if mt_changes:
            secovmt = int(obj_3.secovmt)
            new_vsietevmt = (secovmt + mask2) * 13
            for i in range(1000):
                mid = int(glb.ObMT[i])
                qty = int(glb.nObMT[i])
                if mid > 0 and qty > 0:
                    new_vsietevmt += (i * 13) + (mid * 43) + (qty * 26)
            replacements['obj_3.vsietevmt'] = new_vsietevmt
            print(f"    [*] Checksum de MTs recalculado: vsietevmt={new_vsietevmt}")

    # F. Inyección de Pokémon en Cajas del PC (recalcula vsietecj y vsietecj2)
    if box_pokemon:
        modified_boxes = set()
        num_cajas = int(glb.NumCajas)
        base_date = int(glb.lastDateStored) if int(glb.lastDateStored) > 0 else 121649369
        next_uid = int(glb.fy_001) if int(glb.fy_001) > 0 else 100
        for spec in box_pokemon:
            raw_box = spec.get('box', 3)
            c = num_cajas if str(raw_box).lower() == 'last' else int(raw_box)
            if c < 1 or c > num_cajas:
                raise ValueError(f"Caja {c} fuera de rango (1..{num_cajas}).")
            slot = spec.get('slot', None)
            if slot is None:
                for j in range(30):
                    if int(glb.boxpkmn[c, j]) == 0:
                        slot = j
                        break
            if slot is None:
                raise ValueError(f"La Caja {c} está llena (30/30).")
            slot = int(slot)

            pk_id = int(spec['pkmn_id'])
            if pk_id == 0:
                field_vals = {
                    'boxpkmn': 0, 'boxnivel': 0, 'boxexp': 0, 'boxIV': 0,
                    'boxobjpoke': 0, 'boxpkmnsex': 0,
                    'boxat1': 0, 'boxat2': 0, 'boxat3': 0, 'boxat4': 0,
                    'boxselue_pk': -1,
                    'boxinfo0': 0, 'boxinfo1': 0, 'boxinfo2': 0, 'boxinfo3': 0,
                    'boxinfo4': '', 'boxinfo5': '',
                    'boxinfo6': 0, 'boxinfo7': 0, 'boxinfo8': 0,
                    'boxinfo9': 0, 'boxinfo10': 0, 'boxinfo11': 0, 'boxinfo12': 0,
                    'boxinfo13': 0, 'boxinfo14': 0, 'boxinfo15': 0,
                }
                for fname, fval in field_vals.items():
                    getattr(glb, fname)[c, slot] = fval
                    replacements[f'glb.{fname}[{c},{slot}]'] = fval
                modified_boxes.add(c)
                print(f"[-] Caja {c} Slot {slot + 1}: limpiado.")
                continue

            lvl = max(1, min(100, int(spec.get('level', 42))))
            exp = int(spec.get('exp', lvl ** 3))
            iv = max(0, min(999999, int(spec.get('iv', 999999))))
            item_id = int(spec.get('item_id', 0))
            sex = int(spec.get('sex', 1))
            atks = list(spec.get('attacks', [17, 197, 41, 16])) + [0, 0, 0, 0]
            a1, a2, a3, a4 = int(atks[0]), int(atks[1]), int(atks[2]), int(atks[3])
            aux_mask = (mask1 + 7 + 5000) if (mask1 + 7 < 5000) else (mask1 + 7)
            aux_ntv = int(spec.get('ntv', 999999))
            selue = int(spec.get('selue', ((aux_mask - abs(pk_id)) * 1000000) + aux_ntv))
            isep = int(spec.get('isep', 50))
            nick = str(spec.get('nickname', ''))
            ot = str(spec.get('ot', ''))
            ball = int(spec.get('ball', 2))  # 0=PokéBall, 1=Super, 2=Ultra, 3=MasterBall (ver Script 2845!)
            next_uid += 1

            field_vals = {
                'boxpkmn': pk_id, 'boxnivel': lvl, 'boxexp': exp, 'boxIV': iv,
                'boxobjpoke': item_id, 'boxpkmnsex': sex,
                'boxat1': a1, 'boxat2': a2, 'boxat3': a3, 'boxat4': a4,
                'boxselue_pk': selue,
                'boxinfo0': ball, 'boxinfo1': lvl, 'boxinfo2': 19, 'boxinfo3': 0,
                'boxinfo4': nick, 'boxinfo5': ot,
                'boxinfo6': isep, 'boxinfo7': base_date, 'boxinfo8': base_date,
                'boxinfo9': 255, 'boxinfo10': 0, 'boxinfo11': 0, 'boxinfo12': 0,
                'boxinfo13': isep, 'boxinfo14': selue, 'boxinfo15': next_uid,
            }
            for fname, fval in field_vals.items():
                getattr(glb, fname)[c, slot] = fval
                replacements[f'glb.{fname}[{c},{slot}]'] = fval

            modified_boxes.add(c)
            label = spec.get('name', f'ID {pk_id}')
            print(f"[+] Caja {c} Slot {slot + 1}: {label} (ID {pk_id}) Nv.{lvl} IV={iv} Atks=[{a1},{a2},{a3},{a4}]")

        glb.fy_001 = next_uid
        replacements['glb.fy_001'] = next_uid

        for c in sorted(modified_boxes):
            v7_1 = 0
            for j in range(30):
                v7_1 += (j * 2) + (int(glb.boxpkmn[c, j]) * 11) + (int(glb.boxnivel[c, j]) * 7) + int(glb.boxexp[c, j]) + 131
            v7_1 += (((int(obj_3.secocj[c]) + mask3) * 43) + ((29 + mask2) * 3 * c))
            obj_3.vsietecj[c] = v7_1
            replacements[f'obj_3.vsietecj[{c}]'] = v7_1

            v7_2 = 0
            for j in range(30):
                v7_2 += (j * 2) + (int(glb.boxIV[c, j]) * 13) + 41
                v7_2 += (j * 4) + (int(glb.boxobjpoke[c, j]) * 23) + 41
                v7_2 += (j * 3) + (int(glb.boxpkmnsex[c, j]) * 15) + 41
                v7_2 += (j * 5) + (int(glb.boxselue_pk[c, j]) * 16) + 41
                v7_2 += (j * 7) + (int(glb.boxat1[c, j]) * 11) + 41
                v7_2 += (j * 9) + (int(glb.boxat2[c, j]) * 12) + 41
                v7_2 += (j * 6) + (int(glb.boxat3[c, j]) * 19) + 41
                v7_2 += (j * 8) + (int(glb.boxat4[c, j]) * 14) + 41
            v7_2 += (((int(obj_3.secocj2[c]) + mask2) * 23) + ((19 + mask1) * 2 * c))
            obj_3.vsietecj2[c] = v7_2
            replacements[f'obj_3.vsietecj2[{c}]'] = v7_2
            print(f"    [*] Checksums Caja {c} recalculados: vsietecj={v7_1}, vsietecj2={v7_2}")

    # G. Entrenamiento Extremo Total del Equipo Actual (EVs=999999 + Genética/Chapa Dorada=999999)
    if max_party_stats:
        party_changed = False
        for i in range(6):
            if int(glb.pkmn1[i]) > 0:
                glb.IV[i] = 999999
                replacements[f'glb.IV[{i}]'] = 999999
                prefix = int(glb.selue_pk1[i]) // 1000000
                new_selue = prefix * 1000000 + 999999
                glb.selue_pk1[i] = new_selue
                replacements[f'glb.selue_pk1[{i}]'] = new_selue
                party_changed = True
                print(f"[+] Equipo Slot {i + 1} (ID {int(glb.pkmn1[i])}): EVs=999999 | Entrenamiento Extremo=999999 (selue={new_selue})")
        if party_changed:
            calc_pk2 = (((int(obj_3.secopk2) + mask1) * 7) + ((15 + mask2) * 6))
            for i in range(6):
                calc_pk2 += (i*7) + (int(glb.PP_1[i])*6) + (int(glb.PS_1[i])*7) + int(glb.STD1[i]) + 361
                calc_pk2 += (i*3) + (int(glb.IV[i])*7) + (int(glb.objpoke1[i])*6) + (int(glb.selue_pk1[i])*11) + int(glb.pkmnsex1[i]) + 361
                calc_pk2 += (i*7) + (int(glb.PP_2[i])*6) + (int(glb.PS_2[i])*7) + int(glb.STD2[i]) + 361
                calc_pk2 += (i*3) + (int(glb.IV2[i])*7) + (int(glb.objpoke2[i])*6) + (int(glb.selue_pk2[i])*11) + int(glb.pkmnsex2[i]) + 361
                for j in range(1, 5):
                    calc_pk2 += int(glb.attack1[i, j]) * 7 * j
                    calc_pk2 += int(glb.attack2[i, j]) * 7 * j
                v1 = round(glb.vel1[i] * 100)
                v2 = round(glb.vel2[i] * 100)
                calc_pk2 += (i*13) + (((int(glb.actual1)+8)*5) + (int(glb.MAX_PP_1[i])*2) + (int(glb.MAX_PS_1[i])*2) + (int(glb.XTRA_PS_1[i])*2) + (int(glb.atk1[i])*3) + (int(glb.def1[i])*3) + (v1 * 7))
                calc_pk2 += (int(glb.atk_sp1[i])*5) + (int(glb.def_sp1[i])*3) + (int(glb.prec1[i])*4) + (int(glb.tipoA1[i])*6) + (int(glb.tipoB1[i])*5) + (int(glb.tipoC1[i])*4)
                calc_pk2 += (i*13) + (((int(glb.actual2)+8)*5) + (int(glb.MAX_PP_2[i])*2) + (int(glb.MAX_PS_2[i])*2) + (int(glb.XTRA_PS_2[i])*2) + (int(glb.atk2[i])*3) + (int(glb.def2[i])*3) + (v2 * 9))
                calc_pk2 += (int(glb.atk_sp2[i])*5) + (int(glb.def_sp2[i])*3) + (int(glb.prec2[i])*4) + (int(glb.tipoA2[i])*6) + (int(glb.tipoB2[i])*5) + (int(glb.tipoC2[i])*4)
            calc_pk2 = int(calc_pk2) % 1000000
            obj_3.vsietepk2 = calc_pk2
            replacements['obj_3.vsietepk2'] = calc_pk2
            print(f"    [*] Checksum de Equipo recalculado: vsietepk2={calc_pk2}")

    # 3. Aplicar parche binario sobre el stream completo
    pos = 0
    new_data = bytearray()
    new_acs = 11

    def ex_9342_patch(tag=None):
        nonlocal pos, new_acs
        start = pos
        assert orig_data[pos] == 31; pos += 1
        ln = orig_data[pos]; pos += 1
        if ln == 250:
            rlen = orig_data[pos]; pos += 1
            s = "".join(chr(m_10010[orig_data[pos+i]]) for i in range(rlen))
            pos += rlen
            old_val = int(float(s))
            old_acs = rlen
        else:
            neg = False
            if ln >= 128:
                neg = True
                ln -= 128
            v = 0; mul = 1
            for i in range(ln):
                b = m_10010[orig_data[pos]]; pos += 1
                v += b * mul
                mul *= 256
            if neg: v = -v
            old_val = v
            old_acs = abs(int(v)) % 241
        
        if tag is not None and tag in replacements:
            new_val = replacements[tag]
            raw_b, acs_contrib = encode_num(new_val)
            new_data.extend(raw_b)
            new_acs += acs_contrib
            return new_val
        else:
            new_data.extend(orig_data[start:pos])
            new_acs += old_acs
            return old_val

    def ex_9343_patch(tag=None):
        nonlocal pos, new_acs
        start = pos
        assert orig_data[pos] == 31; pos += 1
        ln = orig_data[pos] | (orig_data[pos+1] << 8); pos += 2
        chars = []
        old_acs = 0
        for i in range(1, ln + 1):
            b = m_10008[orig_data[pos]]; pos += 1
            chars.append(chr(b))
            old_acs += (b * 7) + i
        old_val = "".join(chars)
        
        if tag is not None and tag in replacements:
            new_val = replacements[tag]
            raw_b, acs_contrib = encode_str(new_val)
            new_data.extend(raw_b)
            new_acs += acs_contrib
            return new_val
        else:
            new_data.extend(orig_data[start:pos])
            new_acs += old_acs
            return old_val

    def check_acs_patch(seed):
        nonlocal pos, new_acs
        assert orig_data[pos] == 31; pos += 1
        orig_data[pos]; pos += 1
        calc_acs = int(new_acs) % 251
        new_data.append(31)
        new_data.append(calc_acs)
        new_acs = int(seed)
        return True

    def ex_p(fn, *args):
        if fn == 9342: return ex_9342_patch(*args)
        if fn == 9343: return ex_9343_patch(*args)
        if fn == 8141: return args[0] in (4, 5)
        return 0

    locs_p = {
        'ex': ex_p, 'check_acs': check_acs_patch,
        'glb': DynamicState(), 'obj_3': DynamicState(), 'obj_18': DynamicState(),
        'obj_66': DynamicState(), 'obj_266': DynamicState(), 'obj_325': DynamicState(),
        'obj_331': DynamicState(), 'obj_518': DynamicState(), 'obj_1003': DynamicState(),
        'obj_1198': DynamicState(), 'obj_1330': DynamicState(), 'instance': DynamicState(),
    }

    code_patch = open(RUN_LOADER_PATH, encoding="utf-8").read()
    code_patch = code_patch.replace("glb.dinero=ex(9342)", "glb.dinero=ex(9342, 'glb.dinero')")
    code_patch = code_patch.replace("obj_18.ingreso=ex(9342)", "obj_18.ingreso=ex(9342, 'obj_18.ingreso')")
    code_patch = code_patch.replace("obj_18.cuentacorriente=ex(9342)", "obj_18.cuentacorriente=ex(9342, 'obj_18.cuentacorriente')")
    code_patch = code_patch.replace("obj_18.ev_1434=ex(9342)", "obj_18.ev_1434=ex(9342, 'obj_18.ev_1434')")
    code_patch = code_patch.replace("obj_3.secodin=ex(9342)", "obj_3.secodin=ex(9342, 'obj_3.secodin')")
    code_patch = code_patch.replace("obj_3.vochodin=ex(9342)", "obj_3.vochodin=ex(9342, 'obj_3.vochodin')")
    code_patch = code_patch.replace("obj_3.vsietedin=ex(9343)", "obj_3.vsietedin=ex(9343, 'obj_3.vsietedin')")
    code_patch = code_patch.replace("obj_3.secoban=ex(9342)", "obj_3.secoban=ex(9342, 'obj_3.secoban')")
    code_patch = code_patch.replace("obj_3.vochoban=ex(9342)", "obj_3.vochoban=ex(9342, 'obj_3.vochoban')")
    code_patch = code_patch.replace("obj_3.vsieteban=ex(9343)", "obj_3.vsieteban=ex(9343, 'obj_3.vsieteban')")
    code_patch = code_patch.replace("obj_3.secovob=ex(9342)", "obj_3.secovob=ex(9342, 'obj_3.secovob')")
    code_patch = code_patch.replace("obj_3.vsietevob=ex(9342)", "obj_3.vsietevob=ex(9342, 'obj_3.vsietevob')")
    code_patch = code_patch.replace("obj_3.secovbl=ex(9342)", "obj_3.secovbl=ex(9342, 'obj_3.secovbl')")
    code_patch = code_patch.replace("obj_3.vsietevbl=ex(9342)", "obj_3.vsietevbl=ex(9342, 'obj_3.vsietevbl')")
    code_patch = code_patch.replace("obj_3.secovmt=ex(9342)", "obj_3.secovmt=ex(9342, 'obj_3.secovmt')")
    code_patch = code_patch.replace("obj_3.vsietevmt=ex(9342)", "obj_3.vsietevmt=ex(9342, 'obj_3.vsietevmt')")

    code_patch = code_patch.replace("glb.ObItem[i]=ex(9342)", "glb.ObItem[i]=ex(9342, f'glb.ObItem[{i}]')")
    code_patch = code_patch.replace("glb.nObItem[i]=ex(9342)", "glb.nObItem[i]=ex(9342, f'glb.nObItem[{i}]')")
    code_patch = code_patch.replace("glb.ObBall[i]=ex(9342)", "glb.ObBall[i]=ex(9342, f'glb.ObBall[{i}]')")
    code_patch = code_patch.replace("glb.nObBall[i]=ex(9342)", "glb.nObBall[i]=ex(9342, f'glb.nObBall[{i}]')")
    code_patch = code_patch.replace("glb.ObMT[i]=ex(9342)", "glb.ObMT[i]=ex(9342, f'glb.ObMT[{i}]')")
    code_patch = code_patch.replace("glb.nObMT[i]=ex(9342)", "glb.nObMT[i]=ex(9342, f'glb.nObMT[{i}]')")
    code_patch = code_patch.replace("glb.fy_001=ex(9342)", "glb.fy_001=ex(9342, 'glb.fy_001')")
    code_patch = code_patch.replace("obj_3.vsietecj[i]=ex(9342)", "obj_3.vsietecj[i]=ex(9342, f'obj_3.vsietecj[{i}]')")
    code_patch = code_patch.replace("obj_3.vsietecj2[i]=ex(9342)", "obj_3.vsietecj2[i]=ex(9342, f'obj_3.vsietecj2[{i}]')")
    code_patch = code_patch.replace("obj_3.vsietepk2=ex(9342)", "obj_3.vsietepk2=ex(9342, 'obj_3.vsietepk2')")
    code_patch = code_patch.replace("glb.IV[i]=ex(9342)", "glb.IV[i]=ex(9342, f'glb.IV[{i}]')")
    code_patch = code_patch.replace("glb.selue_pk1[i]=ex(9342)", "glb.selue_pk1[i]=ex(9342, f'glb.selue_pk1[{i}]')")

    for bf in ('boxpkmn', 'boxnivel', 'boxexp', 'boxIV', 'boxobjpoke', 'boxpkmnsex',
               'boxat1', 'boxat2', 'boxat3', 'boxat4', 'boxselue_pk',
               'boxinfo0', 'boxinfo1', 'boxinfo2', 'boxinfo3',
               'boxinfo6', 'boxinfo7', 'boxinfo8', 'boxinfo9', 'boxinfo10',
               'boxinfo11', 'boxinfo12', 'boxinfo13', 'boxinfo14', 'boxinfo15'):
        code_patch = code_patch.replace(f"glb.{bf}[i,j]=ex(9342)", f"glb.{bf}[i,j]=ex(9342, f'glb.{bf}[{{i}},{{j}}]')")
    for bf in ('boxinfo4', 'boxinfo5'):
        code_patch = code_patch.replace(f"glb.{bf}[i,j]=ex(9343)", f"glb.{bf}[i,j]=ex(9343, f'glb.{bf}[{{i}},{{j}}]')")

    exec(code_patch, locs_p, locs_p)
    new_data.extend(orig_data[pos:])
    
    # 4. Guardar archivo en vivo y backup de partida
    with open(SAVE_PATH, 'wb') as f:
        f.write(new_data)
    with open(SAVE_BK_PATH, 'wb') as f:
        f.write(new_data)
    print(f"\n[OK] Partidas actualizadas con éxito:")
    print(f"  -> {SAVE_PATH}")
    print(f"  -> {SAVE_BK_PATH}")

    # 5. Validación automática
    print("\n--- Ejecutando verificación de seguridad integral ---")
    ok, msg = verify_save(SAVE_PATH)
    if ok:
        print(f"[OK] {msg}")
        print("\n>>> ¡INYECCIÓN 100% EXITOSA, SEGURA Y SIN ANOMALÍAS! <<<")
        return True
    else:
        print(f"[ERROR EN VERIFICACIÓN] {msg}")
        # Revertir
        shutil.copy2(os.path.join(b_dir, "reloaded1.savc"), SAVE_PATH)
        shutil.copy2(os.path.join(b_dir, "reloaded1_bk.savc"), SAVE_BK_PATH)
        print("[!] Se ha restaurado el respaldo original por seguridad.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inyector Seguro para Pokémon Reloaded")
    parser.add_argument("--dinero", type=int, help="Cantidad de dinero en mano (ej: 999999)")
    parser.add_argument("--banco", type=int, help="Cantidad de dinero en banco (ej: 1000000)")
    parser.add_argument("--masterballs", type=int, help="Cantidad de Master Balls")
    parser.add_argument("--ultraballs", type=int, help="Cantidad de Ultra Balls")
    parser.add_argument("--caramelos", type=int, help="Cantidad de Caramelos Raros")
    parser.add_argument("--vitaminas", type=int, help="Cantidad de cada vitamina (Proteína, Hierro, etc.)")
    parser.add_argument("--mts", action="store_true", help="Inyectar pack de MTs de Tienda y Casino")
    parser.add_argument("--item", nargs=2, action="append", metavar=('ID', 'CANTIDAD'), help="Añadir objeto por ID y cantidad")
    parser.add_argument("--team-box6", action="store_true", help="Inyectar Equipo Élite de Aventura en la Caja del PC 6")
    parser.add_argument("--max-party", action="store_true", help="Aplicar Entrenamiento Extremo (EVs=999999 + Genética/Chapa Dorada=999999) a todo tu equipo actual")

    args = parser.parse_args()

    # Si se pasan argumentos por línea de comandos
    if any([args.dinero, args.banco, args.masterballs, args.ultraballs, args.caramelos, args.vitaminas, args.mts, args.item, args.team_box6, args.max_party]):
        items_c = []
        if args.item:
            for it_id, it_cnt in args.item:
                items_c.append((int(it_id), int(it_cnt)))
        box_pk = [dict(p, box=6, slot=idx) for idx, p in enumerate(ADVENTURE_DREAM_TEAM)] if args.team_box6 else None
        execute_injection(
            dinero=args.dinero,
            banco=args.banco,
            masterballs=args.masterballs,
            ultraballs=args.ultraballs,
            caramelos=args.caramelos,
            vitaminas=args.vitaminas,
            items_custom=items_c,
            mts=args.mts,
            box_pokemon=box_pk,
            max_party_stats=args.max_party
        )
    else:
        print("=== INYECTOR SEGURO Y JUSTIFICADO - POKÉMON RELOADED ===")
        print("1. Paquete de Inicio Recomendado (10 Master Balls, 50 Caramelos, 500k Dinero, 1M Banco)")
        print("2. Solo Master Balls Justificadas")
        print("3. Solo Caramelos Raros")
        print("4. Paquete de Vitaminas para Maxear Stats (Proteínas, Hierro, Calcio, Carbohidratos, Zinc, Más PS)")
        print("5. Solo Dinero y Banco al Máximo")
        print("0. Salir")
        opc = input("\nElige una opción (0-5): ").strip()
        if opc == '1':
            execute_injection(dinero=500000, banco=1000000, masterballs=10, caramelos=50, ultraballs=50)
        elif opc == '2':
            cnt = int(input("¿Cuántas Master Balls deseas?: "))
            execute_injection(masterballs=cnt)
        elif opc == '3':
            cnt = int(input("¿Cuántos Caramelos Raros deseas?: "))
            execute_injection(caramelos=cnt)
        elif opc == '4':
            cnt = int(input("¿Cuántas unidades de cada vitamina deseas?: "))
            execute_injection(vitaminas=cnt)
        elif opc == '5':
            execute_injection(dinero=999999, banco=1000000)
        else:
            print("Operación cancelada.")
