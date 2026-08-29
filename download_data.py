import os
import requests

# Define target paths and their respective GDrive IDs
FILES_TO_DOWNLOAD = {
    # Root doc
    "AI_Intern_Assignment.pdf": ("1j0de6-bk-BKR4mT5RvgCs3jIyJBbUKZk", "file"),
    
    # follow up
    "Data_set/follow_up_update/01_cafe_music_update.txt": ("1Gequj2T5URS-AxNtIFUVFKmBHO6Bc6zn", "file"),
    
    # hirer conversations
    "Data_set/hirer_conversations/01_cafe_music_whatsapp.txt": ("1LIFUyvkZ2e8PwIdsxM0dktIb0afPo20u", "file"),
    "Data_set/hirer_conversations/02_skincare_photography_chat.txt": ("1JGeAulgUaDlFSRAlX6OL-tpa5u2OTShr", "file"),
    "Data_set/hirer_conversations/03_vertical_video_email.txt": ("1DJR7ccUhfPDPDKMnNLT3GanQZ8TWnSrc", "file"),
    "Data_set/hirer_conversations/04_leadership_event_photos.txt": ("12vLR3-mv_KavUGgv22oaYiawW1Ck_sKH", "file"),
    
    # Musicians profiles and media
    "Data_set/artist_profiles/musicians/M01_Meera_Arjun/profile.txt": ("1qTXfTsBXdH4-SE-JgOeggoHqzcRvDv8ycjl3yrUXHzU", "gdoc"),
    "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/35860-408654164.mp4": ("118wuAUuOvfjcE20GzObinMXbEsLQFHH0", "file"),
    "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/35863-408654169.mp4": ("1agax94_UZ2sR-jrbN8cS6fKRidBeetCJ", "file"),
    "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/35865-408654178.mp4": ("13VAIjrg02BYvx2kL5R-Dpbk7mjY7PGuy", "file"),
    "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/35868-408654193.mp4": ("1NpFIFB5eqmePiiJo11YyARtKmwHo4eEu", "file"),
    "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/MA_cafe_demo_take1.wav": ("1TYzHKqypIBW8lRb8n9IKYOayv1fQLX5K", "file"),
    "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/MA_upbeat_medley_rehearsal.wav": ("1lhTyK1hfuu_GWzdhq5GviJASNKPYg1LN", "file"),
    
    "Data_set/artist_profiles/musicians/M02_Neon_Junction/profile.txt": ("1NfcPrmvUB3a4yjCcEOuoouoU2GbI_vnsBU2O-RVYzxc", "gdoc"),
    "Data_set/artist_profiles/musicians/M02_Neon_Junction/media/ahsleysnow-feel-like-home-523056.mp3": ("1sNuv5BF9v1fVTzusQRi64mH6-t1gGU0y", "file"),
    "Data_set/artist_profiles/musicians/M02_Neon_Junction/media/alex-morgan-downtempo-chill-electronic-528322.mp3": ("1BYJuoGF1cwfz31vvg8fhRpARG0-KkRaq", "file"),
    "Data_set/artist_profiles/musicians/M02_Neon_Junction/media/holodr3ams-pretty-when-i-fall-419712.mp3": ("1T7PQGL9gDYsVIUL_ZXVvjyP7MaaRbNjT", "file"),
    "Data_set/artist_profiles/musicians/M02_Neon_Junction/media/sub_clair-electronic-586100.mp3": ("1bJ2LNA9QCVPSIpDBepovq7RoMtMVJQeA", "file"),
    
    "Data_set/artist_profiles/musicians/M03_Raghav_Sen/profile.txt": ("1M2BPI5TDw-KHqhnyqB6MCBXJYqNFxMoo31uDSo0r5SA", "gdoc"),
    "Data_set/artist_profiles/musicians/M03_Raghav_Sen/media/alanajordan-letting-go-342368.mp3": ("1dLQdDg_FcRY_qtVepUokt2vIyPGSFgFO", "file"),
    "Data_set/artist_profiles/musicians/M03_Raghav_Sen/media/folk_acoustic-summer-walk-152722.mp3": ("17SnjHe59zicvknpm0pcysT6hGDN3rRUb", "file"),
    "Data_set/artist_profiles/musicians/M03_Raghav_Sen/media/swantwirls-quotthe-shared-moonquot-french-male-vocals-ballad-slow-489373.mp3": ("1m9pLoOiVtT-tJEcAEnhxt0rw_jPIvdaS", "file"),
    
    "Data_set/artist_profiles/musicians/M04_KillRush/profile.txt": ("1322aL6zkBy7TCJLVgFXGBpWnyBSjD_qJzj6A4gt4a1k", "gdoc"),
    "Data_set/artist_profiles/musicians/M04_KillRush/media/VID_20260820_214956_321.mp4": ("1PsgSL5hzLakWIvIjfClVFlicE8ZHOOF0", "file"),
    "Data_set/artist_profiles/musicians/M04_KillRush/media/VID_20260820_215053_667.mp4": ("1FagXEkELuCrdcOZKPmQwW81KVumRCy8r", "file"),
    "Data_set/artist_profiles/musicians/M04_KillRush/media/VID_20260820_215432_704.mp4": ("1hizNx-EfNv6LgD-LERXfyOwxE7vXYxQE", "file"),
    "Data_set/artist_profiles/musicians/M04_KillRush/media/VID_20260820_215633_211.mp4": ("1lAmqW00n--X7HWeVrwgvl6Jk-IZDeRe-", "file"),
    "Data_set/artist_profiles/musicians/M04_KillRush/media/VID_20260820_215739_384.mp4": ("1kK2fyA05cVKGgH62ftdUbyecnA7H_Rp6", "file"),
    
    "Data_set/artist_profiles/musicians/M05_Lunar_Noise/profile.txt": ("1qAPCPce22A8L04hWWmF9bZVMI9UGkzL73ZHYAH2Y8yE", "gdoc"),
    "Data_set/artist_profiles/musicians/M05_Lunar_Noise/media/VID_20260820_220359_022.mp4": ("1Ggb1yK70lAU9CaAL5_jD8UjuTimLwZU8", "file"),
    "Data_set/artist_profiles/musicians/M05_Lunar_Noise/media/VID_20260820_220500_334.mp4": ("1S0syfCwOy0jFxxxhiZW0-o5pVi8PvzWq", "file"),
    "Data_set/artist_profiles/musicians/M05_Lunar_Noise/media/VID_20260820_220534_412.mp4": ("1hut2ihVkmT6o7AiyTuhx2kUfWUkVgczW", "file"),
    "Data_set/artist_profiles/musicians/M05_Lunar_Noise/media/VID_20260820_220736_918.mp4": ("1BhjSAZB9w_RHH62ZJ0uS6iqbf3KWp4Pn", "file"),
    "Data_set/artist_profiles/musicians/M05_Lunar_Noise/media/VID_20260820_220933_637.mp4": ("1hOhdRKFhmSwjiehZkclqQsPI1DVrJxnf", "file"),
    "Data_set/artist_profiles/musicians/M05_Lunar_Noise/media/VID_20260820_221016_264.mp4": ("16_UlxF28cCVKFVrKjWakLdUist1mCubl", "file"),
    "Data_set/artist_profiles/musicians/M05_Lunar_Noise/media/VID_20260820_221046_879.mp4": ("1sU1C3S37F53dZ29Q8euoOBSsdLp6JVxP", "file"),
    
    # Photographers profiles and media
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/profile.txt": ("16jU_NgZW85W0PpAstf2NS0Msc5WfYaSwm_PFnXTB8YU", "gdoc"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/587772091_18388610977181645_5390859402103325237_n.jpg": ("1lWvjZxpnzynF-QypQi1rUelJHWPwpB7Z", "file"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/588248682_18388610974181645_2768095694106311115_n.jpg": ("1KdNK9n_jwBtGXS8Ax-Sqty36MpSCxHDr", "file"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/654876028_18440827159113295_420923875456327857_n.jpg": ("1vaF3nFbsYE2KtFVPrjmwsm5L-ZWq3sGh", "file"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/655181081_18440827168113295_5764439845250431447_n.jpg": ("1bPSzO1MOWe6puO6livAWSxE7aIhXAOaX", "file"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/655263876_18223863544312302_4251431796425398007_n.jpg": ("1hrLsPb06q6O5WiOq6EK9TsuexXyV5oo4", "file"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/655871751_18118340938718334_6115286600173335271_n.jpg": ("1xFGr-UqJQ2YtHkoZaobWqlraoe3f3DGd", "file"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/655967139_18223863535312302_3072422796630024834_n.jpg": ("1vQigU69Mz08OddBxFGJfYg5bPjaYLceb", "file"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/655967441_18440827258113295_1893808236507166776_n.jpg": ("1YvKjNldQ1IAE8OfNLwBMpjGZqp3PLyP_", "file"),
    "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/675457826_18371412484203219_8002499830836553801_n.jpeg": ("149dptvvcGvMc-WywWoOnTBxEnMYtOGhg", "file"),
    
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/profile.txt": ("173orWaop1mwL6K79Ihe8UE4wSWmY-fYuAAdrf2GaEME", "gdoc"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/581888523_18149152837419095_6510529012749050816_n.jpg": ("11t3Spgo2JQoCxRHTgTIrALh0yzfq7tIv", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/584395302_18193975549332430_7589282168204267782_n.jpg": ("1nq80pVkQch0ufxPFRQO3-Z8tMrNkz_WY", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/589130604_18193975528332430_8271070466375639613_n.jpg": ("1KHDlA3Wx3Fw69ywxHC1Iikvc7NJyhG0i", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/609878058_18084106841154787_5898780034346918704_n.webp": ("1ADRg8ghz76vEgnFOnkafUiNk-Y0JsqGz", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/610850380_18084106811154787_2749123973287611292_n.webp": ("17w84tSIY7idkgTxZ8GA3k4A_8XLNgmeR", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/610905695_18084106829154787_7361777869458644219_n.webp": ("1iCPqBtsZ54WNbwyIkhqLUvpxjSS2TrQO", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/613639637_18553028863065157_8205418550002430739_n.jpg": ("1YUDXTrNMr28qNepLu_f3UHmArAgDCh5O", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/639869357_17932048743192375_4392999254381444166_n.jpg": ("1wXEu0vlUN4tM5p5vhdH5f5TzedpFh7cb", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/736198656_17935296702298321_4359188965840404264_n.webp": ("14ZbjaFlck_v2t9mXfUaDNmlmv_OX_LNf", "file"),
    "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/740611437_17935296723298321_4282121541708096718_n.webp": ("1njIGs5-no-S3MjhIwLuIeNDNpDk6udZU", "file"),
    
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/profile.txt": ("1J6vdF62bc4LmABm9kN5TOc9KaLdO9lwkMjlNrK76fBA", "gdoc"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/472955981_18135833542377008_469825668246561939_n.jpg": ("1j1AUx8oZe6-FQMopINjlb_wPEe2VukeT", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/474898919_18135833524377008_7619101935522501329_n.jpg": ("1c_dIZYRD4fC9eIbsPSy01ahJt_i2CpAi", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/495094082_18480800233070732_5072622893058829221_n.jpg": ("13neO8MqzFWMn3lxMmW8JXM65m50ZdiKB", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/495129960_18480800263070732_1441767438525505640_n.jpg": ("1TrP2Izfp7YjhSGz91LHTxtKRL2ly_Ybt", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/568535953_18048233270659994_1343407068267753818_n.jpg": ("1cNxG-cnc_S8nQ9wB8tyRTEoOn6BAerE_", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/568686047_18048233231659994_3453830850745898476_n.jpg": ("1cBj1qtRh0RN-axJi1JZwZzH3-FOfxcdE", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/588015115_18384570037150306_6415235776310417168_n.jpg": ("1tliDs1Upa7-_-up4cSlXS6Y4IZFHXTRa", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/588875732_18384570010150306_5108195024455140251_n.jpg": ("13vLSn9Z-Bm-vt_aDVUap9VYtUm832Pvs", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/591146619_18384570076150306_6294007189183836383_n.jpg": ("12_xeDudsztivBcEhKvJFTbji4MmCvx5l", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/618633014_18053520836690799_1299306511778703052_n.jpg": ("1NPiM-PyOard8GmPXtG7dTSLnVHWFIvoG", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/619268337_18053520857690799_6505388170890118659_n.jpg": ("1QaSS6nZvTzUscZqIyU94-BjYQmookwMV", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/629021163_18423227311136512_2126157066924389219_n.jpg": ("1JvW9FhJcTZFXNGNQY9yC2wvsQGbijjcf", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/642493804_18423227320136512_5463720996443682399_n.jpg": ("18cplpF6VX5kBuqzxvCmfjwUQwMCYtwKQ", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/649227877_18042522989768372_5990373176719744775_n.jpeg": ("190LzkHt0lyuvVRDAEClJ3lPHktS30JZh", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/650059065_18041748788754101_1209241736054735372_n.jpg": ("1ugvKbiO4AYRLVc1kW6cjnCZAB3CNOkCd", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/650705980_18035810165785669_4607825306108029841_n.jpg": ("1pIxJ1SEUO_4TjQpxwn3Wa8yWjQHIjjDf", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/659570145_18344121970246912_2217014772362720485_n.jpg": ("1irvPI8Y6aJ1iiV7ApWblubTC1lVBGTxJ", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/669846967_18582977938049031_939833814684061084_n.jpg": ("1_ZlKji7qxLSrNNfmZOGifeXQIb_oERNV", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/670407402_18582978019049031_2721621531588605481_n.jpg": ("1Xw9JEkIkmifSyG0ldczP7BSUQtOV_Uns", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/671859657_17867330172668192_6491356872221587879_n.jpg": ("1BLnGM4zPXI6E6HygSC7Oul16uCgli6oW", "file"),
    "Data_set/artist_profiles/photographers/P03_Leena_Thomas/media/672410974_18458332354102359_8802881131142943485_n.jpg": ("1tCtC96h2E2WS2bqzCkLJNCfvtaZ-bzAV", "file"),
    
    "Data_set/artist_profiles/photographers/PO4_Drift/Drift_Artist_Profile.docx": ("1IU2bhpmPcIRoqta7olns9UABF5XibWqW", "file"),
    "Data_set/artist_profiles/photographers/PO4_Drift/media/20250923T183847233ZUTCimage0.png": ("1FdEVfQdHEeT5DYCXISqUJkFIoisi0NCc", "file"),
    "Data_set/artist_profiles/photographers/PO4_Drift/media/20250923T184357748ZUTCimage0.png": ("1ZK_8vCQzfV8N0oEALqGUb7sJkHx5gT84", "file"),
    "Data_set/artist_profiles/photographers/PO4_Drift/media/20250924T064005020ZUTCimage0.png": ("1-nTrz89J3XUz-zfBQ2mrs0O9Ygn53Z9a", "file"),
    "Data_set/artist_profiles/photographers/PO4_Drift/media/20250925T125803554ZUTCimage0.png": ("14b90v452tgTwT9fnLtrgC5ryy0xdxblZ", "file"),
    
    "Data_set/artist_profiles/photographers/PO5_Frames/Frame_Artist_Profile.docx": ("1StHdMjLbUb98HhZj6pIqjRvZDYIfnJVZ", "file"),
    "Data_set/artist_profiles/photographers/PO5_Frames/media/36c2003b-aa0f-4e10-8950-facba57cd706Sunflower_20251227040241.jpeg": ("1y3s8WKZc0wePaFAtazhQtLV6dnD8UAR5", "file"),
    "Data_set/artist_profiles/photographers/PO5_Frames/media/875ac26c-f559-4a85-8fad-6bd4d5dae2e504_Two_Worlds_One_Smile_Monojit_Dutta-1_20251227033830.jpg": ("1XSoyHn03jKxBaTAQWl9RyrxxPZIZcy9-", "file"),
    "Data_set/artist_profiles/photographers/PO5_Frames/media/20250720T201756066ZUTC352c0d6f-7e85-44d6-968c-37c505a1ef4c.jpg": ("1fVgLotUyPpSoJ4Yzsjxrz8MARSgsBf-U", "file"),
    "Data_set/artist_profiles/photographers/PO5_Frames/media/20250720T202151397ZUTCa86353ed-8705-4600-b7c0-d16ee62733c2.jpg": ("167eR9jPwnoQa3bD_12MstJFacUf0ukcz", "file"),
    "Data_set/artist_profiles/photographers/PO5_Frames/media/20250720T202449728ZUTC4f82bf1e-7884-45f5-8b42-608dde96b1db.jpg": ("15FspJB--6EftFq_5PBseqknd-fS0Z0EQ", "file"),
    "Data_set/artist_profiles/photographers/PO5_Frames/media/20250811T215431642ZUTCf01f13d7-c534-4067-bb63-f24ba353158e.jpg": ("1n4gEMlPKT9mQsZRDYUShgknl_kRHQb21", "file"),
    "Data_set/artist_profiles/photographers/PO5_Frames/media/20250811T220343256ZUTC25f3203f-9b7a-4bc9-86b3-488e7efddcc9.jpg": ("1-Hxh8r83X7Fw55x4jafdqj4Y0e4OrHXF", "file"),
    "Data_set/artist_profiles/photographers/PO5_Frames/media/20250813T161646030ZUTC6bcfaa33-a853-4464-959a-4d066856b159.jpg": ("1meAaUABNLyAe4sWDo-LsOT3pi5tyKq8K", "file"),
    
    # Video Editors
    "Data_set/artist_profiles/video_editors/V01_Nisha_Kapoor/profile.txt": ("1VFSy-Ae2-m5rfM-8PuG9q_qvM0-0FjdsfIbnvB9f9po", "gdoc"),
    "Data_set/artist_profiles/video_editors/V01_Nisha_Kapoor/media/Video-1382.mp4": ("1DI0pt0t5BywGOTOI3JC2nn6toN8GVN8Y", "file"),
    "Data_set/artist_profiles/video_editors/V01_Nisha_Kapoor/media/Video-11391.mp4": ("1MCGwzH45AJ-bz9LtoGnUoQjOacaNQpQo", "file"),
    "Data_set/artist_profiles/video_editors/V01_Nisha_Kapoor/media/Video-42290.mp4": ("1uVyyMh4YPQOc2bMGs5IdvYdwzGhb3GSe", "file"),
    "Data_set/artist_profiles/video_editors/V01_Nisha_Kapoor/media/Video-43513.mp4": ("1zyYBSsNBzIl-xJg0rgzP3qDJVRUt2Dw7", "file"),
    "Data_set/artist_profiles/video_editors/V01_Nisha_Kapoor/media/Video-69962.mp4": ("1fkoO2_OKgWoueXYIj8ueFobPuirzmliS", "file"),
    "Data_set/artist_profiles/video_editors/V01_Nisha_Kapoor/media/Video-82861.mp4": ("1h0L04NHGc9hmAZsB-cS3dI7wxQXgFtxw", "file"),
    "Data_set/artist_profiles/video_editors/V01_Nisha_Kapoor/media/Video-84802.mp4": ("1h-IRDoripT2dkb3xaNl6J6vwORLpThwe", "file"),
    
    "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/profile.txt": ("1Cyk0En_0llb52gEimp4w-VjJ8y1jpM8TGMkp-JwTYHA", "gdoc"),
    "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/media/Video-5523.mp4": ("1-0WquU5Xg_ZqgQX9Zz2wruIqun6KRWjE", "file"),
    "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/media/Video-9403.mp4": ("1H7v5DJXGIGR2I8F-EYZxfc0ds3yI51TL", "file"),
    "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/media/Video-23970.mp4": ("1HZoGokrf3obzZ5iDbkMAWtB3UUP2bCFY", "file"),
    "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/media/Video-41797.mp4": ("1oGX6eZcEIp7kuNiuL3JthqRrazZBqQWB", "file"),
    "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/media/Video-70182.mp4": ("1Upv1PDjxewm9iRTM1IyVR45WW9AhnLYo", "file"),
    "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/media/Video-75516.mp4": ("1-EWx8FiqeK8W2pAEOADKYOMrRn-9Jaf6", "file"),
    "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/media/Video-77734.mp4": ("1LaGaNpAr4Do3iFmAetJ-EnD9Thacs___", "file"),
    
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/profile.txt": ("1xvIV6kXwHSV3ZcAEPS4L7_27Pow5J1pLsl4omrXhCoI", "gdoc"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-12136.mp4": ("1m1mHXI3YxHxvI67biwpH1ivs_8al6VGl", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-15915.mp4": ("14bRuUJ9iVjyOTKef04GzlgpSk-eWM589", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-28319.mp4": ("1BT5g4BppBXbAjt99y_OQgtM4yfNnvKhM", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-32406.mp4": ("1rKptv2pmEs29TlOZFUI1oKHyjQAwtBBb", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-32465.mp4": ("1REc1sgaRdKZ6F1gLxCP2g7l4LC8KSyVB", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-33770.mp4": ("1iVi1A-1RiQFDAxGb1jKfOkxeDZcMrxCZ", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-45937.mp4": ("1G3ZnX9p-JnWqR0nkjr72-vQLn_LpZljT", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-66106.mp4": ("1F1zlSDmOwH63yNdRCIMaeJ4wXsKzTdcQ", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-70591.mp4": ("1zmcbaPv2tIjFBdIeGIlN5Yo-gapGyG2u", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-73044.mp4": ("1jUS0qz4GWC0P7arS4F-ksMGj9bmUIjT4", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-82620.mp4": ("1xeqChWIEsY0axKPUwQ6wrVF73hs6zAJa", "file"),
    "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-93517.mp4": ("10hh-HlMQc_Kry5sRsNsUT_Ur04wu95Pb", "file"),
    
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Shivam_Artist_Profile.docx": ("1QJCXVAo9Nm9RM76GOSniRbfDdz9zmGJr", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/0df61083-dd4f-4133-923f-4d181237d13a_1000185779.jpg": ("1CLuMkjmWZKFiH562zotNOCWJWXtzlAyC", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/1666cefa-0524-45b6-a064-20b461e1cb20_1000185783.jpg": ("1evY6II-YEIv_UxpCjAvqfgfyX40QX3a5", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/9540acd8-653c-4df5-b65d-a43ef80d7eff_1000185780.jpg": ("10Uiga_6GpGbhY04cEOThZPw4dxIzFHu4", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/88816920-09ae-4f8a-be19-a53a38079314_1000074641.mp4": ("1Xsgj6SWoIVxfIflVbU6raocJTkQQVnB7", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/a03e48d1-2e2c-4495-a100-51cf10da6505_1000185790.jpg": ("1eu7Y_35G0Cb5Dcn7VQoQPWIH9mVI02cs", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/c31b5529-8290-4f38-9802-24ff9e7ff38d_1000185789.jpg": ("1Adg2W0rWIjB0eWiMQy1LDUPts17ISwga", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/d6eaed46-e96b-45d6-a93c-118258b35503_1000181677.mp4": ("19Fr8XyAe-Ia25t6FdEKBG8pSfQyd0vgG", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/dabdcb72-81e8-4980-b4b2-47e883bed011_1000184725.mp4": ("1o7xk0MvE_znBJFMBjEur5ycyf3idJU6n", "file"),
    "Data_set/artist_profiles/video_editors/VO4_Shivam_media/Work/e0d42ba4-a2ef-4f51-804c-ab55ee6335b2_1000167312.mp4": ("1Oah-cbzuh-VQUG2ouDQ1zGnPqboY7T6t", "file"),
    
    "Data_set/artist_profiles/video_editors/VO5_Roshan/Roshan_Artist_Profile.docx": ("10hktzonIYkcKNLv-Bj0FxNK-AV3VKvnn", "file"),
    "Data_set/artist_profiles/video_editors/VO5_Roshan/media/_Music_Events.mp4": ("1Kzb4AaZxzQ-OCynl9Ey3LgkL8Sn_DpNQ", "file"),
    "Data_set/artist_profiles/video_editors/VO5_Roshan/media/4320_Samsung_Event_Videography.mp4": ("1HYvajsmLE1Th359TqN4cIOHZ6NbENHKU", "file"),
    "Data_set/artist_profiles/video_editors/VO5_Roshan/media/4321_Gym_Videography.mov": ("1rCYqDzX1GYj0_by8vdxnR1w_taPDuiZi", "file"),
    "Data_set/artist_profiles/video_editors/VO5_Roshan/media/4322_Music_Video.mov": ("11Nr9BKYZN46fEvXZpNeaSP8lK4RlYGzn", "file"),
    "Data_set/artist_profiles/video_editors/VO5_Roshan/media/4323_Cafe_videography.mov": ("1WGJ18s87xGeap0F26PXvXY01vLwoer6f", "file"),
    "Data_set/artist_profiles/video_editors/VO5_Roshan/media/4331_EDITING_WORK.mp4": ("1-aby_3GE1M8UMIP412TSeeUThFyCq9uV", "file"),
    "Data_set/artist_profiles/video_editors/VO5_Roshan/media/4332_Mini_Vlog_edit.mov": ("1tauTPOxwYnQIrSNc8su-I0E-siQpbjeW", "file"),
    "Data_set/artist_profiles/video_editors/VO5_Roshan/media/4345_BTS_MODI_JI.mp4": ("1Biw23obWNYJ81Txkn9f4cO1WATr2Sdz3", "file"),
}

import time

def download_file(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"Skipping {path} (already downloaded)")
        return True
        
    print(f"Downloading {url} to {path}...")
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    max_retries = 5
    backoff = 2
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded successfully: {path}")
                return True
            else:
                print(f"FAILED: {url} (status: {response.status_code})")
                return False
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"Error on attempt {attempt + 1}/{max_retries} downloading {path}: {e}")
            if attempt < max_retries - 1:
                time.sleep(backoff)
                backoff *= 2
            else:
                print(f"Failed to download {path} after {max_retries} attempts.")
                return False

def main():
    for rel_path, (g_id, g_type) in FILES_TO_DOWNLOAD.items():
        if g_type == "gdoc":
            # For google docs, download as txt
            url = f"https://docs.google.com/document/d/{g_id}/export?format=txt"
        else:
            # For general files, download using export=download
            url = f"https://docs.google.com/uc?export=download&id={g_id}"
            
        download_file(url, rel_path)

if __name__ == "__main__":
    main()
