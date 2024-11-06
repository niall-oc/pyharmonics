from pyharmonics import constants
from pyharmonics.marketdata import BinanceCandleData
from pyharmonics.search import HarmonicSearch
from pyharmonics.technicals import OHLCTechnicals
import pandas as pd

b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000, None, None)
b.df = pd.read_pickle("tests/data/btc_test_data")
t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=10)
h = HarmonicSearch(t, fib_tolerance=0.03)
h.search()
h.forming()

def test_xabcd_search():
    assert (len(h._formed[constants.XABCD]) == 6)
    results = sorted([i.p_id for i in h._formed[constants.XABCD]])
    expected = sorted([
        '40e6cf64339bbf28bdf07a530d2dabba6811aa5ad48a6e59fca81f263752d4a4',
        '8c3e58d7bb6ab68f75932e67529f3523ce1385fa751d727a288fb883feee5143',
        'af808e283d6e5593cfb4eeb9737fe8fcb07e32ad385b6dabdc85d1a23f610135',
        'af808e283d6e5593cfb4eeb9737fe8fcb07e32ad385b6dabdc85d1a23f610135',
        'f914364cf2318dfb155a574ed683c0e3715104d68e73f3ca3ac5374f86b4a599',
        'f914364cf2318dfb155a574ed683c0e3715104d68e73f3ca3ac5374f86b4a599'
    ])
    assert (expected == results)


def test_abcd_search():
    assert (len(h._formed[constants.ABCD]) == 6)
    results = sorted([i.p_id for i in h._formed[constants.ABCD]])
    expected = sorted([
        '07d5f1812bf1ee9592c867a393f0603b6f5e8617c3155aed5c8ede9fd670315b',
        '6392d7ecf8b6cf73a4b41b654acfd04a76f17e83f8808b2c0e790ca440e61009',
        'b559cc64d57cc9018c2592bdac418c9c80e59757ec802a072f7bfc5d8b27d4e5',
        'bbb41e571657554d3e846d35b37d3147c253c4619c92749d7139abeb14c609ce',
        'c14865a396e8caefee13cfa6f33f214c084dadf5548276107d6b12cb71e4f96e',
        'e451e3be41c3b2e80849239bc14cd71d3c726204c1bbdf57790c5ad3018afe05'
    ])
    assert (expected == results)


def test_abc_search():
    assert (len(h._formed[constants.ABC]) == 62)
    results = sorted([i.p_id for i in h._formed[constants.ABC]])
    expected = sorted([
        '02b01a17872a4a683361e53573ad5907ef3541104ec868675118d076e2a14950',
        '0806bda93c720c439298795e9caf2968b757571a970cbaeca1ee3ea196af5504',
        '098c47c65893175b938764f5e6138f3934ed28bfedbf2d9cb38d33bd6a496404',
        '0fe55f0858bdf6c0e563c803bc8208321dab82aebb1ec63ba1a7644e4aeee4d9',
        '140d70c5eb879d25e407faaa8b181a082daf6da79816f22fa4f440b97603f959',
        '14cfcc470de58dd46b66355523d534a3b6255c5958f7ad4590aac615272c72f4',
        '1510ce0c2c3e293d0ddb5daf5e17661b7423118e1b0628b5655fc8757fefb478',
        '1510ce0c2c3e293d0ddb5daf5e17661b7423118e1b0628b5655fc8757fefb478',
        '171e9082d80403305b80861dedff4862e70b92a030fc2a0a94e6d357a32610f2',
        '25e13c06f4380e551648666c466b249fb7aba92992ce63e2a8cc5070ee71f8a4',
        '2f399e32367240ecc446c10102f0f81c7ba83016df766a8966547e0c0737e38f',
        '32b51d3c436cce70df355408010772625f61adfdd2d7738a81bc0c06263f5caa',
        '372bf6b0338ee329c51c0a812efcf4e898333ca3593e268aa599e372807275d9',
        '39db0227d327e2ea4603a228c4265e1574af58d5a8792cdf66779e0a2a057384',
        '3b59d8d2e5f1dc558864498c83e49ac6091cc63f222966aafad99d823692137d',
        '3b63491fb5d1b266a9d61a68264afb796253a5e6e675a75b47bc533f5f32531d',
        '3ec627e5159c496969215b8a7da7faef8f03bddaac4610314359f10d99500187',
        '3f049fe854dc55fdd19dd87af1c941e616f70ef3de45f2e0056ebeccfd372c14',
        '4a383fd8280a942b11c5fd40abc333a77585445d25590bd946220ac96e957999',
        '51ed6ffbe4d58a1e9315c502913d16579900ae0c82a00b172fbad1ccc41fc384',
        '60f0b54f0f03140cc42ac65942b5d12eb076fe77949f5e257d1b2444b139ab24',
        '69021abfa382a2e5beda80c62e4fc1b8bde5005fc4dfa09c2d62c2db1778bc0c',
        '6f7c68c5f6636b100b20965ef084349ace5f6c347353d74f654bf4e8db29cc8d',
        '7497fe0f7fa5f3ab144e856514593c9cd655d9de902746d95869d76a8c358cb8',
        '753e214f2bb5e3cf8f4f9eca4be2a852c170c4115be60bf4504e06d0636c12e2',
        '75da0b1dfac3cf38a1ac2d91962538776f163421499b37afa84ee39c08b79089',
        '78993a44b03bb4c6e58491f68b2eb628aaadeadc18dba14a5ed1a466df27c2a4',
        '7c2568fd19b17cf58b3a818726d1116c8643c924458f5d8e79d370e822e4db21',
        '8070d33e56e6ab2247c1d742c60fe151a34e33461aa7a6a8f042d99514d6a77b',
        '865e775e1b79d083b3522f535e49f5db36d2372f900069c7c312361294f81285',
        '874308e597a65212b3a39c0f8a5c99842d76c57fee834dd307ff0a67ac02996c',
        '8b468a6ea40848e95a3addd1b34caef0be3c9901821b3fb42d6f1146be0157ba',
        '8e86a1aa9936c3b37e2844a9ec07fdcb3d382c554dffe19f38e4da641b1221f9',
        '8eeb838b6add2952686661b6bf9f9d53f55f39ed9ef2f7c7e9bbdc680790d6c7',
        '8f428a4ed0415f5f7f73a749a29e6cfb3e42fe63f4bac4f6c3e817fca442f5d7',
        '9090450b7e5dbd0651040d012d7be2f0642dbbcb73190b424ec195a14b07dbb9',
        '935ead7679d9c54aa1c6dd487f8bfd7be89f020701386e977ff67afd5797ea7f',
        '94018c285bc6dd3528f36b21989d51cb26620e04feedb7c2fb16db081b5c76c3',
        '969f80c0d99edf9210621f4b223e9d126c4bbd7e88c50b4bcf18f4af4b478169',
        '97d822d9eec9098bc71e21afb25cf4f5d28711d9c13bafe6bee943fb18791868',
        '9c908f5fda6cecd626a89244f1efef1da7f505b402afa219cebd4dacc5ed92fa',
        'a82a813fec1b3530927df3e15b56d11e66906c0947df5a82a04e40aaf37d64cb',
        'aaa5c0ea508d1d93d136d973c37e7e03877acf4b788c9daf1d44c7cc168fea3b',
        'aba3f6d2420d447236d823075f36b9b2b47afc8852111cd7c3954c23e042499c',
        'abd44abb0eecf0a07ace926e1d7cc2b7185367dde980cf41362ba132d0617c41',
        'aca20d27b1353fc88e1b243418ffaac335e120c961879933737f7d1fa9ad8bb4',
        'b02230f276a2665a17689d2661f1efc67dc61a60dca1093371f4774941d7da9a',
        'b7e778efd7eac5014e2e7423766619543fe3176432522dc996e1745d7f848c0e',
        'bd809596796a3fbb36862f0a09ab180fbfe175386c2683388c3352c490e296f1',
        'bdf4c0c1f149d05361af069c5b06be6966ffb2df8fc4669f8c2635c9932008c1',
        'c4f84277fa267e59ecb12c048f501cc882bad64bba7f7541af13044911e30886',
        'cabb397fa09be904cde91e75bbfa6ec1692590065581289deef776a4cfb82c54',
        'ce7cc751d869782652cc4876ec7a8b23ba5dae72de0dc6da17f824932368f113',
        'd1028580072eb32919f219a77888635209a5e377d518ed3ce9f7a4057a0796bc',
        'd1e332c69f9a4e127efb86024f7d108df600f1827b011bf08513bffc55948116',
        'd3b43ba72059e0872b407fb6762d9bf31377a66862b054085ccfce4a4af8c9aa',
        'e300b049b33aa04e62a29b96c2489664e764ef191ab932ed143d08beacd42c24',
        'ee64acfd057747389bc1ae850b9945f96a4f34885d29df6fcb0ea271fe93868e',
        'eee1f0294aaa67216a97eb401fe5a84e5da09a7735d39fe6b768e5b9986b4903',
        'f56dd9e2c4463853587eb84737f58db1fe1b9a8c4aab02174d266059a31950ab',
        'fa4025049282746a5a7fa067899855e516b7a157d3b2127e165c6d155cc6895f',
        'faf3ddd59c146d141c5c1cd8e0ef8f0f174d2998404618506fc90c0f164e8363'
    ])
    assert (expected == results)


def test_xabcd_forming():
    assert (len(h._forming[constants.XABCD]) == 5)
    results = sorted([i.p_id for i in h._forming[constants.XABCD]])
    expected = sorted([
        '127b8fb7ef98651e5524d3d27c7b8318fd560b28e484c3556347152bba29a4c0',
        '4f05844748cc1c7f6985530574d0258e0426f9e2990a9d86118f0934a7be93a0',
        '97e5f4a5ef56b7c12dd8c7b47ee4e32ddd44843de1c11f03434eac3a7d61bb14',
        'ee85f86ec85de95f4c153a3af0ea9f20d64ba72f1207b2454ff460133eddde08',
        'ee85f86ec85de95f4c153a3af0ea9f20d64ba72f1207b2454ff460133eddde08'
    ])
    assert (expected == results)


def test_abcd_forming():
    assert (len(h._forming[constants.ABCD]) == 11)
    results = sorted([i.p_id for i in h._forming[constants.ABCD]])
    expected = sorted([
        '02a2bf8b586d2c69a1d721993614f934ccc51f1dc1de47921e961a842ebb083b',
        '084081f1484c3dd82a2b61e42ca3e730e26302b6a5a3bf6a1799a3a10c485671',
        '084081f1484c3dd82a2b61e42ca3e730e26302b6a5a3bf6a1799a3a10c485671',
        '10318760820b55462b5b93b65087db67e0d46f990f6543242a0f79e0c7a85756',
        '1b3fffd8ed30a5e59151413aa751ebc4a10547c314d0bd640bac45aac26cf956',
        '1e8fa1270eb2f6de7d25f4e30f59201919f43961b0bcd1f0cd2f3ef2e0b24697',
        '311291b286e66686b07b6a6f531d5b43aff7da3b7bde827d551d718c20940c18',
        '4d7936e0b1b2578834ad286aba58b6309850564c1165c0f19679a4713705ab66',
        '8f1c84b6723d50f0835db95736a20104bb43c614267bda459cfdb171f4a98de0',
        'bbb41e571657554d3e846d35b37d3147c253c4619c92749d7139abeb14c609ce',
        'e04d2c33acdff56a9807c07f44d34bece09bc3fbd8f41bfef0b97844e5a9d8f8'
    ])
    assert (expected == results)
