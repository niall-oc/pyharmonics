from pyharmonics import constants
from pyharmonics.marketdata import BinanceCandleData
from pyharmonics.search import MatrixSearch
from pyharmonics.technicals import Technicals
import pandas as pd

b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000, None, None)
b.df = pd.read_pickle("tests/data/btc_test_data")
t = Technicals(b.df, peak_spacing=10)
m = MatrixSearch(t, fib_tolerance=0.03)
m.search()
m.forming()

def test_xabcd_search():
    assert (len(m._formed[constants.XABCD]) == 6)
    results = sorted([i.p_id for i in m._formed[constants.XABCD]])
    expected = sorted([
        '45a32949a257c05749fe6217566587c0511a80b63d3b8696fbdd694cfe57165e',
        'cd7e5bf24c8019f3f006e075ff343f41132877f36c010b5c4ffe11f1a339ab1a',
        'cd7e5bf24c8019f3f006e075ff343f41132877f36c010b5c4ffe11f1a339ab1a',
        'de2835ece5c3e519650ac2d869e8846bb89458bcfeb346da7680fde372613d1d',
        'e92e04e434e7a14e216c3bf87d38675375f8a4801f8a38c04011bf887b10293b',
        'e92e04e434e7a14e216c3bf87d38675375f8a4801f8a38c04011bf887b10293b',
    ])
    assert (expected == results)


def test_abcd_search():
    assert (len(m._formed[constants.ABCD]) == 6)
    results = sorted([i.p_id for i in m._formed[constants.ABCD]])
    expected = sorted([
        '60fb740d66b3e7ff12ed27fcdc9922577286e7b995c5c7fb40bf2886c0036c1c',
        '749064ae1e093a743b0e63ed4ae2bb9eac942fedc8be15cced778c885ec0f865',
        '8f1dc63faac608da97e9375d0b8aa0d7fde643edde7322a2cb9dff1d9ca6ec9f',
        '925a7456820092e2f152fd1142106f1fc75cdc5c9ef9675cb8018d8b188ca21d',
        'dfc0e7a09785d2d0aeffcf3da61c0d943a8a4edef56def22977736fb51db0357',
        'f9b0afcfbe65997ccaae10a73caf78dafae7d3938ba163eef40d5cd1f29cc477',
    ])
    assert (expected == results)


def test_abc_search():
    assert (len(m._formed[constants.ABC]) == 62)
    results = sorted([i.p_id for i in m._formed[constants.ABC]])
    expected = sorted([
        '05f81579fd95c1dfae9eadcc8b4e64dbe13ce2dca0b184060a881320d55f701e',
        '0ba61b32d30cdb8a57f4b8722dc71410c0375482da87cc48cfd6f2a9b5b9de97',
        '133a5f8ae70544cdaca7968c88994cddbc7463d2453922d0ca3cb18d56ab57e2',
        '15e51fc02b998d093506d5bbdbe13c8e9985cb844cecb10f757fb0afdd99123c',
        '186a26b0f3c6fb89bf4f7c629250bd7bfefaf5aa2ad99fe99412420773a75bb2',
        '1f2bdec663cab8f361295a5305e5cb2a0db3d71fa605733195900874e7467b67',
        '1f5870045af5d874b74a8859b1c5eb3878cc7c5e3707805409fc11a75bc5da5e',
        '21af3ea24570fca4590956eb8baf33d81207697ff4e9ae9b7a673b039ac2a969',
        '22830429c62dd6cd1394003c8fbd78f9972d5bc07cd812ec7bbde7f14ca09993',
        '25d02b8ee6ff6547f57b09f2084d81b47162df25fc1bda749586ab3ab21c8354',
        '2bbcb630ff8fc6cf07677cbf9e905df0e90a81252cc61417fb1ed70e6557210a',
        '2e6d4be4a4ffa77d7e762ad7d3211522224f7fa9408648939237ee73d035a04d',
        '350047c467ba7e923b08b4dbfc4ba6046ec70e3f3f7e03bb50f5d9c6d509f7e8',
        '3a07b437a628b8f00725b3083eefc6d07727d3bcaeffc845e613c7728a32911f',
        '4624a3c3d585f3eff34016d04744c3498f8bea20cdce3cf97927c1423fe74e80',
        '482425edfeaf334295360fbc7ad5586a1023ff37631a3db4a1f230fa7cc0eac1',
        '48fcf5aec66e95cabc553111f5fa7ce0b07a80e51007987faa7417afca816120',
        '4cf301dabea1099f43bef0538ab0f0d2bae536c511f133694f0e30bd9222a6f6',
        '4e3032777c7997045988168bc3573cae7ef5208e09a5230a25799285cd234c43',
        '5181e4cdd40b43c6de16757db99b9c08b23f20367a89b6bcf1706ec4beb747ad',
        '5201d37db8400c2ae73ec33a1617da80a2d61f835b4eeed580aeb0c04de809b1',
        '532ed4b481eb9c083fec7f48c19e391767dc892fe30dce1f43c21cf71dac49fe',
        '53a8e46fdb40112aec29aac4574adfc6588a7cfde72d1cfe568e96c92fb49864',
        '54980109ca3b442d74ecd536a651192376dcfa1b550e58e7ce76adcdadd90eec',
        '54980109ca3b442d74ecd536a651192376dcfa1b550e58e7ce76adcdadd90eec',
        '556a7628c218a702b9c3161beca1837ee607bfc08f955b54fd8fedf7356d55d8',
        '57760678add700931f36a93a81b2ff9d0d35cca8b12a01c65aee29c337efc12a',
        '5929d9aebf9bb8256c48b23c1e78c6708d4228c937a2870ea13c556e870e0c5d',
        '599deeeddb198074438c2bc4ac02a59555c9e9fd90ab5411dda6ced0e44e18ef',
        '59cb90980e89b87172a421ae013d85337567bc74826874e3bcc37e07f3fa3e64',
        '5ab52bfeff24e196afe1eff61b172d03c4903d759515a9d3a3cf8f24178280e2',
        '5acd74fa3c8f63388561b59833214cd59850d7d6dbd510234824e2ae36bac711',
        '5cdd35f8c97dfadc8f8f56e6b48f30d7682e3a0ff4836cac7f6a48e694673f40',
        '5dfb44bd62065d25f567947cb82db0cbe4eb10df30f8a0641228fb4d99ec863c',
        '639eb5cc66f20e50a942a3e4d4aeab3cb4649f7d414d0deeabf5201cc8648364',
        '771fe9e90f5a904933eb5d3209e538aefcb12f7e53477ef94ef9aff343463d86',
        '7cf8f3adee4eea82cd862ff172e7a250d24bd43be3bf5e3aa54e2df2d1d1db01',
        '8535c4d9c719286bc96307967b43080a671767e5c081568ec24d56c9a96d2b99',
        '8816ebf04d65dfc59dcfef5e04c8b5bbe93a6b8d5d4b41f5e63c2380abfa9d8e',
        '8a04de0c1f7b1bd2a00d4580b6d9fae7ac8167bc2b8f7b5917a901691b8e7e48',
        '970cb65976cb96214086db91a4bf38ce5c2283b97719c9a2763ae191f6e08e2e',
        'a92742e1b3d8c1eb2ba827ec7d922dc3bb60adb57d79d2aa515f347aa3999cab',
        'ad37ec16fb263da06cbdcef5cd0ec28cc97cc4083368e6057906fe5dd95423c9',
        'b354ed8c824efc53bc9d8a287052456aa552c84162607444e1b6c514bcc89f69',
        'b49da8a71b9a620da609ed52be61e8c506ff2f1568880085ca45bdd0960c0fd9',
        'bb96dbfc51cf5dc0edc212eb6aede54b601cd604dcd71ade71e5bc17b487d07e',
        'bc2974b478941b079f23e31a7fced8d655647cad691686f30cf195c02d750351',
        'bcae96bef452470dd6368557bafea0780f4907b468bbcd3de3a264665595e2b1',
        'c5116650f03a3a9b3dcef10b0ef3cf31273e8c88ec44216f145b6c784d5f344d',
        'c8ed1213fbb06b2b772e605c5afa7ef524451ea95846b46db177f54ea2ba9c50',
        'c97d02c3290140d3dfd6f4ad4e14032c7863ebb783c63a9ac89039d2ee6266df',
        'cf35877b3bbe67d25469311fa09335ece32b13e28667857d012517c3206bbc44',
        'dca054e660e27fa0da04930f1dd8bf7bd6ec343699a00be69e93d0a144288ca1',
        'dfcd54ca0d4e668882c16029328789825e126107a071f58414cc521b982b8d14',
        'dfea81df0becbb551bf2673a9466dd9c57b536e3981745ef9c37966505048819',
        'e1ef0e0a3512164aa7216a65ddce899e0c0859f7f8c60b1c3f8f8b9d991c99bf',
        'e5df49dc3972417907e3e689b51dd6d37e803c6fd9a7a91209f26b557ca4f108',
        'ea77d833524d1bc6b68c12b97a29bc7655ad56e778643d06acafce2ea2660c81',
        'f0e6664a4f29331b68b46c1092c7ec959e82ee7bdcc0edb3e9d004dcb763f5c1',
        'f6fcd9dafec96cea774cea6e01313c80c64311d43d603ab703eff46d5006a4f6',
        'fa5251999cd880574ea74cfa58845058a77d7404cb73f4f7d518214ef3e0e1d6',
        'ff29c3eba8ab2f00ddfc022174376a76efe6c849ad9c92bc36e15be17725b384',
    ])
    assert (expected == results)


def test_xabcd_forming():
    assert (len(m._forming[constants.XABCD]) == 5)
    results = sorted([i.p_id for i in m._forming[constants.XABCD]])
    expected = sorted([
        '01df59d33c9ca703fe2ca5668c685701c35640b2b6d9b37face538b50b7a04ff',
        '7c8e84ccd28e7a1da1d869892c4c3661e3bbcbf31ad8ee86a6eb4ac32415eeba',
        'd609406a360fab94239411201472687c571ea05fc8163c2710d57c36cdc11837',
        'e71a04574e2d51a32b1b17f396a054f1f94a9e329297277929c60863bcc4c8ed',
        'e71a04574e2d51a32b1b17f396a054f1f94a9e329297277929c60863bcc4c8ed',
    ])
    assert (expected == results)


def test_abcd_forming():
    assert (len(m._forming[constants.ABCD]) == 11)
    results = sorted([i.p_id for i in m._forming[constants.ABCD]])
    expected = sorted([
        '0581e47c16ac359e6c60d88bf247a2b85439a4a7b5ded83c4c3b6f0ec6a1280a',
        '2320b6327e3f111bf5d8b9d259b455da86999f7c8a62eebbaee7b97abc7b522a',
        '30466d6e1b8a1b097e85ed5b6c6965d8045ffbe14165ef840ff74fa1c459c422',
        '42b3e6d519e5de49d915900553003cabe2cdbcdf24289e29e5bc3fc82216c4e9',
        '4b809045380410e7c6ccbe5d2e4be061a1c14d57c7ad749305b318276b44a5d8',
        '60fb740d66b3e7ff12ed27fcdc9922577286e7b995c5c7fb40bf2886c0036c1c',
        '743b3bb8b138ce40f751b1c4de5a8074c85ff055698aff3ea1b3bf3c0588e869',
        '7d961b017a4aa6c1804a85e9f8ea37e9976900dc409c7c33579438ff07c51c07',
        '7d961b017a4aa6c1804a85e9f8ea37e9976900dc409c7c33579438ff07c51c07',
        'bbb0fc184fac77fbe98b7d6496302f66d7c1a9215ed8edf6a0d494aa9c0f0943',
        'de5fc031ab82c6a5cb3379f20ab7fb0c07c4f0563437074cfb63378179b427c3',
    ])
    assert (expected == results)
