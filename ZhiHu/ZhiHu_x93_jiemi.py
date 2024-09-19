import hashlib
import random
import sys
from operation import sls, urs, band

'''
写在前面 , 这个破解 X96 的方法,源自  https://github.com/srx-2000 大佬
剩余内容为 根据大佬提供 的解密方法 进行继续编写
'''

x_zse_93 = "101_3_3.0"
# 基础加密字符串，每次从中选择一个字母，最终拼接成加密结果
base_str = "6fpLRqJO8M/c3jnYxFkUVC4ZIG12SiH=5v0mXDazWBTsuw7QetbKdoPyAl+hN9rgE"
# 用于计算后续的G数组中的G[1]，那个16位的数组。
base_arr = [48, 53, 57, 48, 53, 51, 102, 55, 100, 49, 53, 101, 48, 49, 100, 55]
# 在函数__g.r中使用
h_zk = [1170614578, 1024848638, 1413669199, -343334464, -766094290, -1373058082, -143119608, -297228157, 1933479194,
        -971186181, -406453910, 460404854, -547427574, -1891326262, -1679095901, 2119585428, -2029270069, 2035090028,
        -1521520070, -5587175, -77751101, -2094365853, -1243052806, 1579901135, 1321810770, 456816404, -1391643889,
        -229302305, 330002838, -788960546, 363569021, -1947871109]
# 在函数G_f中使用
h_zb = [20, 223, 245, 7, 248, 2, 194, 209, 87, 6, 227, 253, 240, 128, 222, 91, 237, 9, 125, 157, 230, 93, 252,
        205, 90, 79, 144, 199, 159, 197, 186, 167, 39, 37, 156, 198, 38, 42, 43, 168, 217, 153, 15, 103, 80, 189,
        71, 191, 97, 84, 247, 95, 36, 69, 14, 35, 12, 171, 28, 114, 178, 148, 86, 182, 32, 83, 158, 109, 22, 255,
        94, 238, 151, 85, 77, 124, 254, 18, 4, 26, 123, 176, 232, 193, 131, 172, 143, 142, 150, 30, 10, 146, 162,
        62, 224, 218, 196, 229, 1, 192, 213, 27, 110, 56, 231, 180, 138, 107, 242, 187, 54, 120, 19, 44, 117,
        228, 215, 203, 53, 239, 251, 127, 81, 11, 133, 96, 204, 132, 41, 115, 73, 55, 249, 147, 102, 48, 122,
        145, 106, 118, 74, 190, 29, 16, 174, 5, 177, 129, 63, 113, 99, 31, 161, 76, 246, 34, 211, 13, 60, 68,
        207, 160, 65, 111, 82, 165, 67, 169, 225, 57, 112, 244, 155, 51, 236, 200, 233, 58, 61, 47, 100, 137,
        185, 64, 17, 70, 234, 163, 219, 108, 170, 166, 59, 149, 52, 105, 24, 212, 78, 173, 45, 0, 116, 226, 119,
        136, 206, 135, 175, 195, 25, 92, 121, 208, 126, 139, 3, 75, 141, 21, 130, 98, 241, 40, 154, 66, 184, 49,
        181, 46, 243, 88, 101, 183, 8, 23, 72, 188, 104, 179, 210, 134, 250, 201, 164, 89, 216, 202, 220, 50,
        221, 152, 140, 33, 235, 214]


class ZhiHuEncrypt:
    headers = {
        'x-zse-93': x_zse_93,
        'x-api-version': '3.0.91',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-zse-96': '2.0_',
        'accept': '*/*',
    }

    def __init__(self):
        pass

    @staticmethod
    def get_md5_code(un_str: str):
        return hashlib.md5(un_str.encode()).hexdigest()

    @staticmethod
    def get_ord_list(md5_code):
        return [ord(i) for i in md5_code]

    @staticmethod
    def get_Dv_48_list(c_v: list):
        return [int(127 * random.random()), 0] + c_v + [14 for _ in range(0, 14)]

    @staticmethod
    def get_Ev_Fv(d_v: list):
        return d_v[0:16], d_v[16:48]

    @staticmethod
    def get_Jv(e_v):
        return [e_v[i] ^ base_arr[i] ^ 42 for i in range(len(e_v))]

    @staticmethod
    def B_f(tt: list, te: int):
        return sls((255 & tt[te]), 24) | sls((255 & tt[te + 1]), 16) | sls((255 & tt[te + 2]), 8) | 255 & tt[te + 3]

    @staticmethod
    def G_f(tt: int):
        te = [0 for _ in range(0, 4)]
        tr = [0 for _ in range(0, 4)]
        ZhiHuEncrypt.i_f(tt, te, 0)
        # 下方的h_zb是一个固定的256位的数字数组
        tr[0] = h_zb[255 & te[0]]
        tr[1] = h_zb[255 & te[1]]
        tr[2] = h_zb[255 & te[2]]
        tr[3] = h_zb[255 & te[3]]
        ti = ZhiHuEncrypt.B_f(tr, 0)
        return ti ^ ZhiHuEncrypt.Q_f(ti, 2) ^ ZhiHuEncrypt.Q_f(ti, 10) ^ ZhiHuEncrypt.Q_f(ti, 18) ^ ZhiHuEncrypt.Q_f(ti,
                                                                                                                     24)

    @staticmethod
    def i_f(tt: int, te: list, tr: int):
        te[tr] = 255 & urs(tt, 24)
        te[tr + 1] = 255 & urs(tt, 16)
        te[tr + 2] = 255 & urs(tt, 8)
        te[tr + 3] = 255 & tt

    @staticmethod
    def Q_f(tt, te):
        return sls(band(4294967295, tt), te) | urs(tt, 32 - te)

    @staticmethod
    def __g_r(tt: list) -> list:
        te = [0 for _ in range(0, 16)]
        tr = [0 for _ in range(0, 36)]
        tr[0] = ZhiHuEncrypt.B_f(tt, 0)
        tr[1] = ZhiHuEncrypt.B_f(tt, 4)
        tr[2] = ZhiHuEncrypt.B_f(tt, 8)
        tr[3] = ZhiHuEncrypt.B_f(tt, 12)
        for i in range(0, 32):
            ta = ZhiHuEncrypt.G_f(tr[i + 1] ^ tr[i + 2] ^ tr[i + 3] ^ h_zk[i])  # 这里的h_zk同样也是一个固定的32位数组
            tr[i + 4] = tr[i] ^ ta
        ZhiHuEncrypt.i_f(tr[35], te, 0)
        ZhiHuEncrypt.i_f(tr[34], te, 4)
        ZhiHuEncrypt.i_f(tr[33], te, 8)
        ZhiHuEncrypt.i_f(tr[32], te, 12)
        return te

    @staticmethod
    def __g_x(tt: list, te: list) -> list:
        tr = []
        for i in range(0, 2):
            tu = tt[i * 16:(i + 1) * 16]  # 将32位数组切分，16个元素为一组
            tc = [None for _ in range(0, 16)]
            for j in range(0, 16):
                tc[j] = tu[j] ^ te[j]
            te = ZhiHuEncrypt.__g_r(tc)
            tr += te
        return tr

    @staticmethod
    def get_Mv(d_v):
        e_v, f_v = ZhiHuEncrypt.get_Ev_Fv(d_v)
        j_v = ZhiHuEncrypt.get_Jv(e_v)
        k_v = ZhiHuEncrypt.__g_r(j_v)
        l_v = ZhiHuEncrypt.__g_x(f_v, k_v)
        return k_v + l_v

    @staticmethod
    def final_encrypt(m_v):
        encrypt_str = ""
        for i in range(len(m_v) - 1, -1, -3):
            # 这里有四种算法，并且以4个为一组[0,24,16,8]这样循环。
            if i % 4 == 3:
                a_v = (m_v[i] ^ 58) + (sls(m_v[i - 1], 8)) + (sls(m_v[i - 2], 16))  # 此处M_v为基础逻辑中计算得出
            elif i % 4 == 0:
                a_v = m_v[i] + (sls(m_v[i - 1] ^ 58, 8)) + (sls(m_v[i - 2], 16))
            elif i % 4 == 1:
                a_v = m_v[i] + (sls(m_v[i - 1], 8)) + (sls(m_v[i - 2] ^ 58, 16))  # 此处M_v为基础逻辑中计算得出
            else:
                a_v = m_v[i] + (sls(m_v[i - 1], 8)) + (sls(m_v[i - 2], 16))  # 此处M_v为基础逻辑中计算得出
            # a_v = m_v[i] + (sls(m_v[i - 1] ^ 58, 8)) + (sls(m_v[i - 2], 16))  # 此处M_v为基础逻辑中计算得出
            b_v = a_v & 63
            encrypt_str += base_str[b_v]
            c_v = urs(a_v, 6) & 63
            encrypt_str += base_str[c_v]
            d_v = urs(a_v, 12) & 63
            encrypt_str += base_str[d_v]
            e_v = urs(a_v, 18)
            encrypt_str += base_str[e_v]
        return encrypt_str

    @staticmethod
    def encode(a_v):
        b_v = ZhiHuEncrypt.get_md5_code(a_v)
        c_v = ZhiHuEncrypt.get_ord_list(b_v)
        d_v = ZhiHuEncrypt.get_Dv_48_list(c_v)
        m_v = ZhiHuEncrypt.get_Mv(d_v)
        final_encrypt_code = ZhiHuEncrypt.final_encrypt(m_v)
        return final_encrypt_code

    @staticmethod
    def get_96(url: str, d_c0: str):
        a_v = ''
        url_host = "https://www.zhihu.com"
        if url.find('?') != -1:
            url_path = url.split("?")[0].replace(url_host, "") + "?"
            url_params = url.split("?")[1]
            a_v = x_zse_93 + "+" + url_path + url_params + "+" + d_c0
        else:
            a_v = x_zse_93 + "+" + url.replace(url_host, "") + "+" + d_c0
        encrypted_str = ZhiHuEncrypt.encode(a_v)
        ZhiHuEncrypt.headers.update({"x-zse-96": '2.0_' + encrypted_str})
        return '2.0_' + encrypted_str


if __name__ == '__main__':
    a = []
    for i in range(1, len(sys.argv)):
        a.append((str(sys.argv[i])))
    rest = ZhiHuEncrypt.get_96(a[0], a[1])
    print(rest)
