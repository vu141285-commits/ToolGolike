
# from FB_WEB_API import FacebookSession, FB_API, HTMLExtractor, NumberEncoder, CookieHandler, GenData,facebookDapi,GolikeAPI
import threading
import time
import random
import json
import os
import re
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
import sys
import requests

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    # Nếu môi trường (như IDLE) không hỗ trợ reconfigure, ép kiểu mã hóa bằng cách gán trực tiếp hoặc bỏ qua
    import codecs
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
import threading, time, random, json, os, re
console = Console(force_terminal=True)
import types

FB_WEB_API_CODE = r"""
# ===== DÁN TOÀN BỘ CODE FB_WEB_API.py VÀO ĐÂY =====

import requests
import json
import time
import random
import mimetypes
import re,base64
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
class CookieHandler:
    @staticmethod
    def to_dict(cookie_str: str) -> Dict[str, str]:
        return {k.strip(): v.strip() for item in cookie_str.split(";") 
                if "=" in item for k, v in [item.split("=", 1)]}
class NumberEncoder:
    @staticmethod
    def to_base36(num: int) -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        if num == 0:
            return "0"
        result = ""
        while num:
            num, remainder = divmod(num, 36)
            result = chars[remainder] + result
        return result

class HTMLExtractor:
    @staticmethod
    def find_pattern(html: str, pattern: str) -> Optional[str]:
        match = re.search(pattern, html)
        return match.group(1) if match else None
    
    @staticmethod
    def extract_token(html: str) -> Optional[str]:
        patterns = [
            r'DTSGInitialData".*?"token":"([^"]+)"',
            r'"token":"([^"]+)"',
        ]
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result:
                return result
        return None
    @staticmethod
    def extract_lsd(html: str) -> Optional[str]:
        patterns = [
            r'LSD".*?"token":"([^"]+)"',
            r'"token":"([^"]+)"',
        ]
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result:
                return result
        return None
    @staticmethod
    def extract_user_id(html: str) -> Optional[str]:
        patterns = [
            r'"actorID":"(\d+)"',
            r'"USER_ID":"(\d+)"',
            r'c_user=(\d+)',
        ]
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result:
                return result
        return None
    
    @staticmethod
    def extract_revision(html: str) -> Optional[str]:
        pattern = r'client_revision["\s:]+(\d+)'
        return HTMLExtractor.find_pattern(html, pattern)
    
    @staticmethod
    def extract_jazoest(html: str) -> Optional[str]:
        pattern = r'jazoest=(\d+)'
        return HTMLExtractor.find_pattern(html, pattern)
class FacebookSession:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.token = None
        self.user_id = None
        self.revision = None
        self.jazoest = None
    def authenticate(self) -> bool:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "cookie": self.cookie,
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(
                "https://www.facebook.com/",
                headers=headers,
                cookies=CookieHandler.to_dict(self.cookie),
                timeout=30
            )
            
            html = response.text
            self.token = HTMLExtractor.extract_token(html)
            self.user_id = HTMLExtractor.extract_user_id(html)
            self.revision = HTMLExtractor.extract_revision(html) or "1000000"
            self.jazoest = HTMLExtractor.extract_jazoest(html) or "0"
            self.lsd = HTMLExtractor.extract_lsd(html) or "0"
            return {
                "token": self.token or "N/A",
                "user_id": self.user_id or "N/A",
                "revision": self.revision or "N/A",
                "jazoest": self.jazoest or "N/A",
                "lsd" : self.lsd or "N/A",
            }
        except Exception as e:
            return {'err' : f'Lỗi {str(e)}'}
        
class GenData:
    def __init__(self, session: FacebookSession):
        self.session = session
        self.request_counter = 0
    
    def build_REACTION(self, reaction : str, ID_POST:str,doc_id = 'null') -> Dict[str, Any]:
        if doc_id == 'null':
            self.docid = '24198888476452283'
        else:
            self.docid = doc_id
        self.request_counter += 1   
        reaction_id_list = [1635855486666999,1678524932434102,613557422527858,115940658764963,478547315650144,908563459236466,444813342392137,'ERR']
        reaction_id_= reaction_id_list[0] if reaction == "LIKE" else reaction_id_list[1] if reaction == "LOVE" else reaction_id_list[2] if reaction == 'CARE' else  reaction_id_list[3] if reaction  == 'HAHA' else reaction_id_list[4] if reaction == 'WOW' else reaction_id_list[5] if reaction == 'SAD' else reaction_id_list[6] if reaction == 'ANGRY' else reaction_id_list[7]
        if reaction_id_ == "ERR" :
            return {'err' : 'Không Thể Sử Dụng Loại Cảm Xúc Này'}
        
        s = "feedback:"+str(ID_POST)
        self.idpost = base64.b64encode(s.encode("utf-8")).decode("utf-8")
        payload = {
           'av': self.session.user_id,
            '__user': self.session.user_id,
            '__req': NumberEncoder.to_base36(self.request_counter),
            '__rev': self.session.revision,
            'fb_dtsg': self.session.token,
            'jazoest': self.session.jazoest,
            'lsd': self.session.lsd,
            '__spin_r': self.session.revision,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
            'server_timestamps': 'true',
            'variables': '{"input":{"attribution_id_v2":"CometHomeRoot.react,comet.home,via_cold_start,1765901136948,422377,4748854339,,","feedback_id":"'+self.idpost+'","feedback_reaction_id":"'+str(reaction_id_)+'","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"tracking":[],"session_id":"'+str(uuid.uuid4())+'","actor_id":"'+self.session.user_id+'","client_mutation_id":"1"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}',
            'doc_id': self.docid,
        }
        return payload
    def build_PiC(self,filename):
        try:
            subname = mimetypes.guess_type(filename)[0]
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "max-age=0",
                "cookie": self.session.cookie,
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            }
            params = {
                'av': self.session.user_id,
                '__aaid': '0',
                '__user': self.session.user_id,
                '__a': '1',
                '__req': '3o',
                '__hs': '20438.HYP:comet_pkg.2.1...0',
                'dpr': '1',
                '__ccg': 'EXCELLENT',
                '__rev': self.session.revision,
                '__s': 'cbrikq:ac7kkv:8obh3z',
                '__hsi': '7584526071696689530',
                '__dyn': '7xeUjGU9k9wxxt0koC8G6Ejh941twWwIxu13wFw_DyUJ3odF8vyUco5S3O2Saxa1NwJwpUe8hw8u2a1sw9u0LVEtwMw6ywIK1Rwwwg8a8462mcw8a1TwgEcEhwGxu782lwj8bU9kbxS2617wnE6a1awhUC7Udo5qfK0zEkxe2GexeeDwkUtxGm2SU4i5oe8cEW4-5pUfEdbwxwhFVovUaU3qxW2-awLyESE7i3C223908O3216gjxebwHwKG4UrwFg2fK7oC1hxB0jUpwgUjz89oeefx6UabDzUiBG2OUqwjVqwLwHwa211wo83KwHwOyUqxG0HEC',
                '__csr': 'gbsaEQrs2b1d4nPMB5NApnkgyggEtkIr9R4lsGuIpOhdGzFi9TiEgD5sBWi_lvj4bmFBGCAAyQKyviZPiO2jbPUBiXBKjSZWAlkDnbpmKk-iGtlTsDi9WnFV4N5ayeQAAh9aQ9VfaFbjD8h_L_RWjF5Z7iyV9pLXCHyknHVWqAt6VGKHFuHnV2222lUxpF9Ux9rLCFXFRXJ7AJKUDVlJqigBrDmjWQcCJGGGiinyAGKCTDiKHyAAeOvgymnKiaz-WBK8SaCh9penG9KiARiy-EGmiFJd24GjBH9BRyoyiQmdK9ABAzubjrCDxihe_LGQFFrxiqtt96gShz4qbVV4QrmaVGAJumaGXQqQqidAKGK5p8Ku9m8y9QnAiUkgBeuiEylvD-q9m4EmG8BDyKuXG-ah8x3XzKmVToc4cQCegqyDV8Gi58O8gyF4Jbx6aoizUKiElx7AgnBDyElx2iV68Km6oG2m5Edpp9m8BxmcyVrCyeECdABCg-9yEiCxPyk3J16ufgmjxqii4p8vDDACKqqeADzUhU-HggVE6W5Fof8C2i15Fy8C4UO5ogxO0Do5WdGA2268lg5Km5A5ojwUwCyWDxa8-K3y2t0PAyE4O32axC6EiUSqbK9y_iDF0Ag5m4KV7joGqdzbGcxaH8m9YylswK6ooUtg_zFotBAWnyonoS3eiEF2UCt0AXx8HRomgGm2h2Emm3C2h0LxmcxKeDoy6UynBGFFaqxi6AewFgW32t0wxCjXAy-UWFo8UgxS7VeU9E88l-9gqDDo3_wsUtw1pS05L426hTAz259zd5p40BGwnE1080SS0zA0yEaodbz8jwWwBK2Ra2m68nxX80c1w8q05bo492Enw53CgG16wu-0qm2K19nG6E0FG0lC8U2tF011-0aIw11msAE0cRo0axo5C320vwFU09qQuaw0w7wlE2_wL80hdw5BDg9UOu1Ec0W84e2Ly9TwcYxEB2Q1Yw8oM0S128C1gwXo142123ZxG2O04QE4Rw2s8kP3U7Za1Dyo2Ry40yQm0v9fx5G1wwjo1bEy1fwfu6d2C0kBwci0YQ2S0xFT50bi681xo6S2S6UCAqeaA3ei0AAi1Iyp2w9xw2Eopw4oo5Iw9FEW164aIiLuN8ye67wCx-0Wo-5ESaU0spEU0ieg8Vo0z-9S3y0ie0xk1kwgUgyFQ5998nw8C1Hy301HShwlolw821SwYwMooyDw115G5k6cw5la2a0cYo3Hw4Tg1y85y3Ku6EgybQexm0egyxm9gO7Q6IIQZO6hi0lG_g3m87oy9gO9wu86G0UE20wmE0By1vxC',
                '__hsdp': 'g4EwWgt12CAgacW2y58qwMyE4OE5p0FiqphG8xy6NVAzMB4Xkpq2kc9Sg5BPgB2l8l2o-qixG1j9PEbOO48B5W5Fph28IfOOBT5hryQmjrh2jckydPMx8yqqD8Wht8ihmpFIQj2h0AWuwCaaAZ8sDj9bDkix4bN2sxn2kcP9Eh6y8GCHEiax5zkxsQBgAQyJpa8GbqXpnBtJEx4AOBpqCGoF3CBFagxpFxyQJEcSjBiulhVarihd39Cskf4BeO4mQrXFKFupDiBmEGxd5AF4iGAoMDKHcgzienyQZCpYyaiXh6y7pqGF9kyIxTBaAKkHhZkxIzyBF4dHkoggl54KqpOAyEGFAFazXAAAK4y5iKl3SinhACx0CUB9qABWExRyqiyNgCOyFbAgK43GXEMiDrj6kh0woShh8-heHgx4ppQl4gkK4ouJ7V9V9pEy4oigGmFEK315RyUbucO38-nm5kn-yCwwpUXyVUSlWUJ9ipUMqVpS8HxynwLCwFgqG6VZpogG3iby8aUa4uEybzEdE82wjk6k69Quax3wlFUgwFxa1mx6m7e2Ba1lx-dIwGeUfUcohAqcKxfhfg8U88fU8oGi12ogxq7UkgkGewzyUG7Q45O0zG8U9HwxK12xC5qUowOBBglxSElHQ3-2ieGm2Wl2V2wzxGGxe3m0zLoa9VojOqXzUhxe3Kq3KvwPK4u1xAJ289pUow991aehQEmorBwfa5U2twko4-3e0QE5Ku8wgocUqwwwg84Sm7U6G6EswHwai9whEdE7C3K1fwNwIwzx_giwwwSzEd866dwcS2Ki0pi2q7Ebo1hU6214www-xu7oKby8eEcU4e0z83rx-0DU1gVo2cwhk6U6h0gE9EoyE9E-m68dofofUcUeUG48727osxK1hwiU4y0h64oow8e6E8qyEgzo42U31w9a0OQ1qwzxS10wm8cU662y7o26wXwkooK68nxq1Gx61Qz415xN387i3G321Fwio3ewAws8fEf8bi0vAey84G2W4Unw9Cbw8y2bw9mi16CxB0QAw8G1xwqUnwAx20AUuwLxGewn418w8q0BUrw',
                '__hblp': '1yegb8ijIkjh8eUeocU8U96aw961bwBxi5Ejy9HU5K1iw9G2e6EcUnG3y1MK5ojAwOgaUaU22wzxC3G4o5F1TWBxu5qg6Wax2i12Wmbz8gABUJi1e6UhKicx6i5FWxybzo8e2ny8O0yU9V85SfGi5E8WwFxnyoryEy1Ry8hwooa8423W0BK9wXwBUkxq0HFUbWwzwRxS585S2q7UpzUyq222-fCKuaBx26-5Eepo2Ix6m3oC2-3e5qxO1twci2-3e326EDwUy8y5UWdwEDy89U650AwSghxa6EoBwBxu2y2aQ2OFEy224E50w8Utxq48a9o29wTwcq4o46em6E4y8gdEowAwYxibCy8jxu6UK0zE43z85q5UcU9E6iUqwQCyEjzoS7824x-E4G49UrwKK1awwxy8yE4q6FovyUmwiEd8aUtwwGmU9Uc82awKwgF8tyoaEcpF98pzoW4o88bK4U9obEW6Q6EC3u1DyEO58eooxe2KK1owwwHwzx-7o3iy8y6U7y1hwm8qy8dFEgx62Sfxa58wwd8a8myUy2e5E9UswOwionG2u2aEpwhUC9wDxu7UcE4a2CcwQwEwOwlEcEjxui8wjUpUO3y8grwlU9UObzUkx68zUGaxKUKmu48vyUC33LwKwGwn8pyu2l3poC9gkxi8xO8wQwLwiaxueUkyEa8fEkwFwh9olyohxy68S12zUC6EW2248S4A78jxi1ewCgdo6y2C3u0AQ2m5Qm3CfxTxG9y4cwTxe3e5lwhSi2acx25Uyah8ixi8xqqmax-48K1uK645Euxy3iqcyo5G4ECmbomgbohyByA5V5gowVwiEZe8G1qUO3OTO0sUnwygnCCG49GzXwNwGwwxSUgU9rwF82a3iq7QaK8x-dCh8-10UlU7K7oK3e5ofE98G2C362auV8O4U9pEpm8ga98K1oCxV39J163eU5yqbxu2iUOEqwwCgC6oaaC84oW226FVEgwzxzz418w8q8UuyKewhU9o',
                '__sjsp': 'g4EwWgt12CAgacW2y58qwMyE4OE5p0FiqphG8xy6NVAzB94NeR6mxch5N5dSgr5NchsQ9ihJ8l2omD6E5cDewLb8gyknEmBB48yM-yi6T5iOKcBCgEAFD8m_xxAuQFSiEx9oBatFxl1ifxm8gFkFANhnj8utojwxqhVE8QP9EgcgjDCwAgVaqIQB1p0BLACup94zbLU94pwGCgp3eeJ257AKmAu3pyP6hXhEF4yFCtal4zx55Dgy78yP48i74epZ4xpzkcDCEwtzyzAooifx6hk3NOwJwYpAq5QcgcA59oc8C6V4bwkk350bJ07LwmU2zwkU7a0ji0jzwFg2am0sx0n4',
                '__comet_req': '15',
                'fb_dtsg': self.session.token,
                'jazoest': self.session.jazoest,
                'lsd': self.session.lsd,
                '__spin_r': self.session.jazoest,
                '__spin_b': 'trunk',
                '__spin_t': '1765910087',
                '__crn': 'comet.fbweb.CometHomeRoute',
            }
            files = {
                'source': (None, '8'),
                'profile_id': (None, self.session.user_id),
                'waterfallxapp': (None, 'comet'),
                'farr': (filename,open(filename,"rb"),subname),
                'upload_id': (None, 'jsc_c_16'),
            }
            response = requests.post(
             'https://upload.facebook.com/ajax/react_composer/attachments/photo/upload',
                params=params,
                headers=headers,
                files=files,
            )
            r = response.text.replace("for (;;);","")
            json_ = json.loads(r)
          
            if 'payload' in json_ and 'photoID' in json_['payload']:
                return json_['payload']['photoID']
            else:
                return {'err': 'Không tìm thấy photoID trong response'}
        except Exception as e:
            return {'err' : f'Lỗi {str(e)}'}
    def build_CMT(self, cmt : str, ID_POST:str , Group_id : str ,doc_id = 'null') -> Dict[str, Any]:
        if doc_id == 'null':
            self.docid = '24615176934823390'
        else:
            self.docid = doc_id
        s = "feedback:"+str(ID_POST)
        self.idpost = base64.b64encode(s.encode("utf-8")).decode("utf-8")
        payload = {
           'av': self.session.user_id,
            '__user': self.session.user_id,
            '__req': NumberEncoder.to_base36(self.request_counter),
            '__rev': self.session.revision,
            'fb_dtsg': self.session.token,
            'jazoest': self.session.jazoest,
            'lsd': self.session.lsd,
            '__spin_r': self.session.revision,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
            'server_timestamps': 'true',
            'variables': '{"feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"groupID":'+Group_id+',"input":{"client_mutation_id":"3","actor_id":"'+self.session.user_id+'","attachments":null,"feedback_id":"'+self.idpost+'","formatting_style":null,"message":{"ranges":[],"text":"'+cmt+'"},"attribution_id_v2":"CometHomeRoot.react,comet.home,unexpected,1765906156209,334250,4748854339,,;CometPhotoRoot.react,comet.mediaviewer.photo,via_cold_start,1765906141242,783051,,82,","vod_video_timestamp":null,"is_tracking_encrypted":true,"tracking":[],"feedback_source":"DEDICATED_COMMENTING_SURFACE","idempotence_token":"client:'+str(uuid.uuid4())+'","session_id":"'+str(uuid.uuid4())+'"},"inviteShortLinkKey":null,"renderLocation":null,"scale":1,"useDefaultActor":false,"focusCommentID":null,"__relay_internal__pv__CometUFICommentAvatarStickerAnimatedImagerelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false}',
            'doc_id': self.docid,
        }
        return payload
    def build_Follow(self,USERID:str, doc_id = 'null'):
        if doc_id == 'null':
            self.docid = '32658454793801856'
        else:
            self.docid = doc_id
        payload = {
           'av': self.session.user_id,
            '__user': self.session.user_id,
            '__req': NumberEncoder.to_base36(self.request_counter),
            '__rev': self.session.revision,
            'fb_dtsg': self.session.token,
            'jazoest': self.session.jazoest,
            'lsd': self.session.lsd,
            '__spin_r': self.session.revision,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUserFollowMutation',
            'server_timestamps': 'true',
            'variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1765909558185,660688,250100865708545,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"'+USERID+'","tracking":null,"actor_id":"'+self.session.user_id+'","client_mutation_id":"2"},"scale":1}',
            'doc_id': self.docid,
        }
        return payload
    def build_post(self,TEXT :str , PHOTO, GROUP, doc_id = 'null'):
        self.fb_api_req_friendly_name = 'ComposerStoryCreateMutation'
        if doc_id == 'null':
            self.docid = '25312274141763468'
        else:
            self.docid = doc_id
        if PHOTO != 'null' and GROUP == 'null':
            photo_id = self.build_PiC(PHOTO)
            if 'err' in str(photo_id) and photo_id['err']:
                return photo_id
            var = '{"input":{"composer_entry_point":"inline_composer","composer_source_surface":"newsfeed","composer_type":"feed","idempotence_token":"'+str(uuid.uuid4())+'_FEED","source":"WWW","audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"message":{"ranges":[],"text":"'+TEXT+'"},"inline_activities":[],"text_format_preset_id":"0","publishing_flow":{"supported_flows":["ASYNC_SILENT","ASYNC_NOTIF","FALLBACK"]},"reels_remix":{"is_original_audio_reusable":true,"remix_status":"DISABLED"},"attachments":[{"photo":{"id":"'+str(photo_id)+'"}}],"logging":{"composer_session_id":"'+str(uuid.uuid4())+'"},"navigation_data":{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,1765910390697,887073,4748854339,,"},"tracking":[null],"event_share_metadata":{"surface":"newsfeed"},"actor_id":"'+self.session.user_id+'","client_mutation_id":"3"},"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":true,"renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":true,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__CometUFICommentAvatarStickerAnimatedImagerelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__TestPilotShouldIncludeDemoAdUseCaserelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider":false,"__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider":true,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReels_enable_meta_ai_label_gkrelayprovider":true,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true,"__relay_internal__pv__GroupsCometGYSJFeedItemHeightrelayprovider":150,"__relay_internal__pv__StoriesShouldIncludeFbNotesrelayprovider":false,"__relay_internal__pv__GHLShouldChangeSponsoredAuctionDistanceFieldNamerelayprovider":false,"__relay_internal__pv__GHLShouldUseSponsoredAuctionLabelFieldNameV1relayprovider":false,"__relay_internal__pv__GHLShouldUseSponsoredAuctionLabelFieldNameV2relayprovider":false}'
        elif PHOTO == 'null' and GROUP != 'null':
            var = '{"input":{"composer_entry_point":"inline_composer","composer_source_surface":"group","composer_type":"group","logging":{"composer_session_id":"'+str(uuid.uuid4())+'"},"source":"WWW","message":{"ranges":[],"text":"'+TEXT+'"},"with_tags_ids":null,"inline_activities":[],"text_format_preset_id":"0","group_flair":{"flair_id":null},"composed_text":{"block_data":["{}"],"block_depths":[0],"block_types":[0],"blocks":["test"],"entities":["[]"],"entity_map":"{}","inline_styles":["[]"]},"navigation_data":{"attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,via_cold_start,1766479285443,369314,2361831622,,"},"tracking":[null],"event_share_metadata":{"surface":"newsfeed"},"audience":{"to_id":"'+str(GROUP)+'"},"actor_id":"'+str(self.session.user_id)+'","client_mutation_id":"2"},"feedLocation":"GROUP","feedbackSource":0,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":false,"renderLocation":"group","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":false,"isFundraiser":false,"isFunFactPost":false,"isGroup":true,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__CometUFICommentAvatarStickerAnimatedImagerelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__TestPilotShouldIncludeDemoAdUseCaserelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider":false,"__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider":true,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReels_enable_meta_ai_label_gkrelayprovider":true,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__FBUnifiedLightweightVideoAttachmentWrapper_wearable_attribution_on_comet_reels_qerelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true,"__relay_internal__pv__GroupsCometGYSJFeedItemHeightrelayprovider":206,"__relay_internal__pv__ShouldEnableBakedInTextStoriesrelayprovider":false,"__relay_internal__pv__StoriesShouldIncludeFbNotesrelayprovider":false,"__relay_internal__pv__GHLShouldChangeSponsoredAuctionDistanceFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldUseSponsoredAuctionLabelFieldNameV1relayprovider":true,"__relay_internal__pv__GHLShouldUseSponsoredAuctionLabelFieldNameV2relayprovider":false}'
            self.docid = '25312274141763468' if doc_id == 'null' else doc_id
            self.fb_api_req_friendly_name = 'ComposerStoryCreateMutation'
        elif PHOTO != 'null' and GROUP != 'null':
            photo_id = self.build_PiC(PHOTO)
            if 'err' in str(photo_id) and photo_id['err']:
                return photo_id
            var = '{"input":{"composer_entry_point":"inline_composer","composer_source_surface":"group","composer_type":"group","logging":{"composer_session_id":"'+str(uuid.uuid4())+'"},"source":"WWW","message":{"ranges":[],"text":"'+TEXT+'"},"with_tags_ids":null,"inline_activities":[],"text_format_preset_id":"0","group_flair":{"flair_id":null},"attachments":[{"photo":{"id":"'+photo_id+'"}}],"composed_text":{"block_data":["{}"],"block_depths":[0],"block_types":[0],"blocks":[""],"entities":["[]"],"entity_map":"{}","inline_styles":["[]"]},"navigation_data":{"attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,via_cold_start,1766479285443,369314,2361831622,,"},"tracking":[null],"event_share_metadata":{"surface":"newsfeed"},"audience":{"to_id":"'+str(GROUP)+'"},"actor_id":"'+self.session.user_id+'","client_mutation_id":"3"},"feedLocation":"GROUP","feedbackSource":0,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":false,"renderLocation":"group","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":false,"isFundraiser":false,"isFunFactPost":false,"isGroup":true,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__CometUFICommentAvatarStickerAnimatedImagerelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__TestPilotShouldIncludeDemoAdUseCaserelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider":false,"__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider":true,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReels_enable_meta_ai_label_gkrelayprovider":true,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__FBUnifiedLightweightVideoAttachmentWrapper_wearable_attribution_on_comet_reels_qerelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true,"__relay_internal__pv__GroupsCometGYSJFeedItemHeightrelayprovider":206,"__relay_internal__pv__ShouldEnableBakedInTextStoriesrelayprovider":false,"__relay_internal__pv__StoriesShouldIncludeFbNotesrelayprovider":false,"__relay_internal__pv__GHLShouldChangeSponsoredAuctionDistanceFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldUseSponsoredAuctionLabelFieldNameV1relayprovider":true,"__relay_internal__pv__GHLShouldUseSponsoredAuctionLabelFieldNameV2relayprovider":false}'
            self.docid = '25312274141763468' if doc_id == 'null' else doc_id
            self.fb_api_req_friendly_name = 'ComposerStoryCreateMutation'
        else:
            photo_id = 'null'
            var =  '{"input":{"composer_entry_point":"inline_composer","composer_source_surface":"newsfeed","composer_type":"feed","idempotence_token":"'+str(uuid.uuid4())+'_FEED","source":"WWW","audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"message":{"ranges":[],"text":"'+TEXT+'"},"inline_activities":[],"text_format_preset_id":"0","publishing_flow":{"supported_flows":["ASYNC_SILENT","ASYNC_NOTIF","FALLBACK"]},"reels_remix":{"is_original_audio_reusable":true,"remix_status":"DISABLED"},"logging":{"composer_session_id":"'+str(uuid.uuid4())+'"},"navigation_data":{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,1765912581894,250430,4748854339,,"},"tracking":[null],"event_share_metadata":{"surface":"newsfeed"},"actor_id":"'+self.session.user_id+'","client_mutation_id":"2"},"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":true,"renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":true,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__CometUFICommentAvatarStickerAnimatedImagerelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__TestPilotShouldIncludeDemoAdUseCaserelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider":false,"__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider":true,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReels_enable_meta_ai_label_gkrelayprovider":true,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true,"__relay_internal__pv__GroupsCometGYSJFeedItemHeightrelayprovider":150,"__relay_internal__pv__StoriesShouldIncludeFbNotesrelayprovider":false,"__relay_internal__pv__GHLShouldChangeSponsoredAuctionDistanceFieldNamerelayprovider":false,"__relay_internal__pv__GHLShouldUseSponsoredAuctionLabelFieldNameV1relayprovider":false,"__relay_internal__pv__GHLShouldUseSponsoredAuctionLabelFieldNameV2relayprovider":false}',
        
        payload = {
           'av': self.session.user_id,
            '__user': self.session.user_id,
            '__req': NumberEncoder.to_base36(self.request_counter),
            '__rev': self.session.revision,
            'fb_dtsg': self.session.token,
            'jazoest': self.session.jazoest,
            'lsd': self.session.lsd,
            '__spin_r': self.session.revision,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': self.fb_api_req_friendly_name,
            'server_timestamps': 'true',
            'variables': var,
            'doc_id': self.docid,
        }
        return payload
    
class FB_API:
    def __init__(self, cookie: str,proxy=None):
        self.cookie = cookie
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        self.session = FacebookSession(cookie)
        self.payload_builder = None
        self.ready = False
        # ✅ thêm dòng này
        self.proxies = proxy if isinstance(proxy, dict) else None
    def login(self) -> bool:
        self.info = self.session.authenticate()
        if 'err' in self.info and self.info['err']:
            return self.info
        if self.info:
            self.payload_builder = GenData(self.session)
            self.ready = True
            self.header ={
                "accept": "*/*",
                "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "https://www.facebook.com",
                "referer": "https://www.facebook.com/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": self.ua,
                "x-fb-lsd": self.session.lsd,
                "cookie" : self.cookie,
                'x-fb-friendly-name': 'CometUFIFeedbackReactMutation',
            }
            return True
    def REACTION(self,REACTION : str,Id_post : str, doc_id : str = 'null'):
        pass
        if not isinstance(REACTION, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(Id_post, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(doc_id, str):
            return {"success": False, "error": "Value erorr"}
        try:
            self.login()
            if not self.ready:
                return {"success": False, "error": "Not logged in"}
            payload = self.payload_builder.build_REACTION(REACTION,Id_post, doc_id )
            if 'err' in payload and payload['err']:
                return payload
        
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.header, data=payload,proxies=self.proxies)
            feedback_get_id = response.json().get('data', {}).get('feedback_react', {})
            if response.status_code == 200:
                if feedback_get_id : 
                    feedback_get_id_1 = feedback_get_id.get('feedback',{})
                    feedback_id = feedback_get_id_1.get('id')
                    reaction_count = feedback_get_id_1.get('i18n_reaction_count')
                    return {"success": True, "error" : None , "feedback_id" : str(feedback_id), "reaction_count" : str(reaction_count)}
                else :
                    
                    return {"success": False, "error" : str(response.json()) }
           
            else:
                return {"success": False, "error" : str(response.status_code)}
           
        except Exception as e:
             return {"success": False, "error": str(e)}
    def CMT(self,cmt:str,Id_post : str,Group_id:str = 'null', doc_id : str = 'null'):
        pass
        if not isinstance(cmt, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(Id_post, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(Group_id, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(doc_id, str):
            return {"success": False, "error": "Value erorr"}
        try:
            self.login()
            if not self.ready:
                return {"success": False, "error": "Not logged in"}
            payload = self.payload_builder.build_CMT(cmt,Id_post,Group_id, doc_id )
    
            if 'err' in payload and payload['err']:
                return payload
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.header, data=payload,proxies=self.proxies)
            cmt_get_id = response.json().get('data', {}).get('comment_create', {})
            match = re.search(
                r"'comment'\s*:\s*\{[^}]*?'url'\s*:\s*'([^']+)'",
                str(response.json())
            )
            if response.status_code == 200:
                if cmt_get_id and match:
                    total_count = cmt_get_id.get('feedback',{}).get('comment_rendering_instance',{}).get('comments',{}).get('total_count',{})
                    comment_url = match.group(1)
                    return {"success": True, "error" : None , "total_count" : total_count,"comment_url" : comment_url}
                else:
                    return {"success": False, "error" : str(response.json())}
            else:
                return {"success": False, "error" : str(response.status_code)}
        except Exception as e:
             return {"success": False, "error": str(e)}
    def FOLLOW(self,Id_post:str, doc_id:str = 'null'):
        pass
        if not isinstance(Id_post, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(doc_id, str):
            return {"success": False, "error": "Value erorr"}
        try:
            self.login()
            if not self.ready:
                return {"success": False, "error": "Not logged in"}
            payload = self.payload_builder.build_Follow(Id_post, doc_id)
            if 'err' in payload and payload['err']:
                return payload
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.header, data=payload,proxies=self.proxies)
            pattern = r'"profile_owner"\s*:\s*\{[^}]*?"id"\s*:\s*"(\d+)"'
            match = re.search(pattern, str(response.json()))
            
            if response.status_code == 200:
                if match:
                    return {"success": True, "error" : None , "id" : match.group(1)}
                else:
                    return {"success": False, "error" : str(response.json())}
            else:
                return {"success": False, "error" : str(response.status_code)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    def POST(self,content : str,Photo :str = 'null',Group_id :str = 'null', doc_id : str = 'null'):
        pass
        if not isinstance(content, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(Photo, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(Group_id, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(doc_id, str):
            return {"success": False, "error": "Value erorr"}
        try:
            self.login()
            if not self.ready:
                return {"success": False, "error": "Not logged in"}
            payload = self.payload_builder.build_post(content,Photo,Group_id, doc_id )
    
            if 'err' in payload and payload['err']:
                return payload
            
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.header, data=payload,proxies=self.proxies)
            if Group_id != 'null':
                idpost = re.search(r'"post_id"\s*:\s*"(\d+)"', response.text)
            else:
                idpost = re.search(r"'post_id'\s*:\s*'(\d+)'", str(response.json()))
            if response.status_code == 200:
                if idpost:
                    return {"success": True, "error" : None , "id" : idpost.group(1) }
                else:
                    return {"success": False, "error" : str(response.json())}
            else:
                return {"success": False, "error" : str(response.status_code)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    def JOIN_GROUP(self, group_id: str, doc_id: str = 'null'):
        if not isinstance(group_id, str):
            return {"success": False, "error": "Value error"}
        if not isinstance(doc_id, str):
            return {"success": False, "error": "Value error"}

        try:
            self.login()
            if not self.ready:
                return {"success": False, "error": "Not logged in"}

            # 🔥 FIX header đúng mutation + referer
            self.header['x-fb-friendly-name'] = 'GroupCometJoinForumMutation'
            self.header['referer'] = f'https://www.facebook.com/groups/{group_id}/'

            # 🔥 FIX variables (không nối string nữa)
            variables = {
                "feedType": "DISCUSSION",
                "groupID": group_id,
                "input": {
                    "action_source": "GROUP_MALL",
                    "group_id": group_id,
                    "actor_id": self.session.user_id,
                    "client_mutation_id": "1"
                }
            }

            payload = {
                'av': self.session.user_id,
                '__user': self.session.user_id,
                '__req': '1',
                '__rev': self.session.revision,
                'fb_dtsg': self.session.token,
                'jazoest': self.session.jazoest,
                'lsd': self.session.lsd,
                '__spin_r': self.session.revision,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'GroupCometJoinForumMutation',
                'server_timestamps': 'true',
                'variables': json.dumps(variables),
                'doc_id': '26470860599212339' if doc_id == 'null' else doc_id,
            }

            response = requests.post(
                'https://www.facebook.com/api/graphql/',
                headers=self.header,
                data=payload,
                proxies=self.proxies
            )

            # 🔥 DEBUG chuẩn
            # print("STATUS:", response.status_code)
            # print("TEXT:", response.text[:100000])

            try:
                data = response.json()
            except:
                return {
                    "success": False,
                    "error": "NOT JSON (checkpoint / cookie die / blocked)",
                    "raw": response.text[:200]
                }

            join_data = data.get('data', {}).get('group_join_forum', {})

            if response.status_code == 200:
                if join_data.get('success'):
                    return {"success": True, "error": None}
                else:
                    return {"success": False, "error": str(data)}
            else:
                return {"success": False, "error": str(response.status_code)}

        except Exception as e:
            return {"success": False, "error": str(e)} 
    def IS_LIKED(self, object_id: str):
        try:
            variables = {
                "feedbackID": object_id,
                "scale": 1
            }

            data = self._post("24094105923567748", variables)

            if not data:
                return False

            feedback = data.get("data", {}).get("node", {})

            # nếu có reaction → đã like
            reaction = feedback.get("viewer_feedback_reaction")

            return reaction is not None

        except Exception as e:
            # print("IS_LIKED ERR:", e)
            return False
    def IS_JOINED_GROUP(self, group_id: str):
        try:
            url = f"https://www.facebook.com/groups/{group_id}/"

            res = self.session.get(
                url,
                headers={"user-agent": self.ua},
                cookies=self.cookies,
                allow_redirects=True
            )

            # nếu bị redirect → chưa join
            if "join" in res.url or "membership" in res.url:
                return False

            # nếu ở lại group page → đã join
            return True

        except Exception as e:
            # print("IS_JOINED ERR:", e)
            return False    
    def CHECK_REACTION(self, object_id: str):
        try:
            url = f"https://www.facebook.com/{object_id}"

            headers = {
                "user-agent": self.ua,
                "cookie": self.cookie
            }

            res = self.session.get(url, headers=headers, proxies=self.proxies)
            text = res.text.lower()

            # ===== CHECK REACTION =====
            if "remove like" in text or "gỡ thích" in text:
                return "LIKE"
            if "remove love" in text:
                return "LOVE"
            if "remove care" in text:
                return "CARE"
            if "remove haha" in text:
                return "HAHA"
            if "remove wow" in text:
                return "WOW"
            if "remove sad" in text:
                return "SAD"
            if "remove angry" in text:
                return "ANGRY"

            return None

        except Exception as e:
            return {"error": str(e)}    
    def token_reaction(self, object_id, reaction_type, token):
        try:
            url = f"https://graph.facebook.com/v23.0/{object_id}/reactions"

            data = {
                "type": reaction_type,
                "access_token": token
            }

            r = requests.post(url, data=data)
            print("TOKEN:", r.status_code, r.text)

            return r.status_code == 200

        except Exception as e:
            print("TOKEN ERROR:", e)
            return False


    def token_comment(self, object_id, message, token):
        try:
            url = f"https://graph.facebook.com/v23.0/{object_id}/comments"

            data = {
                "message": message,
                "access_token": token
            }

            r = requests.post(url, data=data)
            print("TOKEN:", r.status_code, r.text)

            return r.status_code == 200

        except Exception as e:
            print("TOKEN ERROR:", e)
            return False                     
class JobManager:
    def __init__(self, cooldown_seconds=30):
        self.job_last_access = {}
        self.job_cooldown = cooldown_seconds
        self.job_countdown = {}
        self.paused_jobs = set()

    def pause(self, jobID):
        self.paused_jobs.add(jobID)

    def canAccessJob(self, jobID):
        if jobID in self.paused_jobs:
            return False, -1

        currentTime = time.time()

        if jobID in self.job_countdown:
            countdown_end = self.job_countdown[jobID]
            if currentTime < countdown_end:
                remaining = countdown_end - currentTime
                return False, remaining
            else:
                del self.job_countdown[jobID]

        if jobID in self.job_last_access:
            last_access = self.job_last_access[jobID]
            time_since_access = currentTime - last_access
            if time_since_access < self.job_cooldown:
                remaining = self.job_cooldown - time_since_access
                return False, remaining

        return True, 0

    def markJobAccessed(self, jobID):
        self.job_last_access[jobID] = time.time()

    def setJobCountDown(self, jobID, countdown_seconds):
        self.job_countdown[jobID] = time.time() + countdown_seconds

    def getNextAvailableJob(self, jobs, current_index=0):
        if not jobs:
            return None, 0, 0

        for i in range(len(jobs)):
            idx = (current_index + i) % len(jobs)
            jobID = jobs[idx]
            can_access, remaining = self.canAccessJob(jobID)
            if can_access:
                return jobID, idx, 0

        min_wait = float('inf')
        best_job = jobs[0]
        best_idx = 0
        for i, jobID in enumerate(jobs):
            can_access, remaining = self.canAccessJob(jobID)
            if remaining == -1:
                continue
            if remaining < min_wait:
                min_wait = remaining
                best_job = jobID
                best_idx = i

        return best_job, best_idx, min_wait
class GolikeAPI:

    def __init__(self, token):
        self.token = token

    def get_user_info(self):
        url = "https://gateway.golike.net/api/users/me"
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": f"{self.token}",
            "content-type": "application/json;charset=utf-8",
            "origin": "https://app.golike.net",
            "user-agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()["data"]
            return data
        return None

    def get_fb_info(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'authorization': f"{self.token}",
            'content-type': 'application/json;charset=utf-8',
            'origin': 'https://app.golike.net',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"iOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            't': 'VFZSak0wMTZVWGROVkZrelRtYzlQUT09',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X)',
        }

        params = {
            'limit': '200',
        }

        response = requests.get(
            'https://gateway.golike.net/api/fb-account',
            params=params,
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            fb_list = data["data"]["data"]

        print("===== DANH SÁCH FACEBOOK =====")
        for i, acc in enumerate(fb_list, start=1):
            print(f"{i}. {acc['fb_name']} | UID: {acc['fb_id']} | ID: {acc['id']}")

        return fb_list

    def choose_account(self):
        fb_list = self.get_fb_info()
        choice = int(input("\nChọn số acc muốn chạy job: "))
        acc = fb_list[choice - 1]

        fb_id = acc["fb_id"]

        print("\nAcc đã chọn:")
        print("Tên:", acc["fb_name"])
        print("UID:", fb_id)
        print("Account ID:", acc["id"])

        return acc["fb_id"], acc["id"]

    def get_jobs(self, fb_id):
        base_url = "https://gateway.golike.net/api/advertising/publishers/get-jobs-2026"

        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": f"{self.token}",
            "content-type": "application/json;charset=utf-8",
            "origin": "https://app.golike.net",
            "t": "VFZSak0wMTZVWGROZWxFeVRsRTlQUT09",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X)"
        }

        servers = ["sv1", "sv2", "sv3"]
        index = 0

        while True:
            current_sv = servers[index]
            # print(f"\n Đang check {current_sv}...")

            start_time = time.time()

            while time.time() - start_time < 30:
                
                # 🔥 sv1 không cần param server
                if current_sv == "sv1":
                    url = f"{base_url}?fb_id={fb_id}"
                else:
                    url = f"{base_url}?fb_id={fb_id}&server={current_sv}"

                try:
                    r = requests.get(url, headers=headers, timeout=10)

                    try:
                        data = r.json()
                    except:
                        time.sleep(5)
                        continue

                    jobs = data.get("data", [])

                    if jobs:
                        # print(f" {current_sv} có {len(jobs)} job")

                        # print("\n===== DANH SÁCH JOB =====")
                        # for job in jobs:
                        #     print("Job ID:", job["id"])
                        #     print("Type:", job["type"])
                        #     print("Coin:", job["fix_coin_job"])
                        #     print("Link:", job["link"])
                        #     print("Object ID:", job["object_id"])
                        #     print("---------------------")

                        return jobs , current_sv

                    else:
                        # print(f" {current_sv} chưa có job, đợi 5s...")
                        time.sleep(5)

                except Exception as e:
                    print(f" Lỗi {current_sv}:", e)
                    time.sleep(5)

            # print(f" {current_sv} không có job sau 2 phút → chuyển server")
            index = (index + 1) % len(servers)

    def complete_job(self, job_id, job_type, object_id, uid, fb_account_id, advertising_id=None, retry=True):
        url = "https://gateway.golike.net/api/advertising/publishers/complete-jobs-2026"

        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": self.token if "Bearer" in self.token else f"Bearer {self.token}",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://app.golike.net",
            "t": getattr(self, "t_token", ""),
            "user-agent": "Mozilla/5.0",
        }

        json_data = {
            "object_id": str(object_id),
            "job_id": int(job_id),
            "type": job_type,
            "uid": str(uid),
            "users_fb_account_id": int(fb_account_id),
            "users_advertising_id": int(advertising_id or job_id),
            "message": None,
            "retry": retry
        }

        try:
            res = requests.post(url, headers=headers, json=json_data, timeout=20)
            data = res.json()

            # ======================
            # DEBUG RAW
            # ======================
            # print("STATUS:", res.status_code)
            # print("RAW:", res.text)

            # ======================
            # PARSE SAFE
            # ======================
            success = data.get("success", False)
            status = data.get("status", res.status_code)

            msg = (
                data.get("message")
                or data.get("skip", {}).get("msg")
                or data.get("error")
                or "NO_MESSAGE"
            )

            # lấy xu nếu có
            coin = None
            if isinstance(data.get("data"), dict):
                coin = data["data"].get("prices")

            # ======================
            # LOG
            # ======================
            # if success:
            #     if coin:
            #         # print(f"✔ COMPLETE SUCCESS +{coin} xu | {msg}")
            #     else:
            #         # print(f"✔ COMPLETE SUCCESS | {msg}")
            # else:
            #     # print(f"❌ COMPLETE FAIL | {msg}")

            return {
                "success": success,
                "status": status,
                "message": msg,
                "coin": coin,
                "raw": data
            }

        except Exception as e:
            # print("❌ ERROR:", e)
            return {
                "success": False,
                "message": str(e)
            }
    def report_job(self, users_advertising_id, fb_id):
        url = "https://gateway.golike.net/api/report/send"

        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json;charset=UTF-8",
            "authorization": self.token if "Bearer" in self.token else f"Bearer {self.token}",
        }

        data = {
            "description": "Tôi không muốn làm Job này",
            "users_advertising_id": int(users_advertising_id),
            "type": "ads",
            "fb_id": str(fb_id),
            "error_type": 0,
            "provider": "facebook",
            "comment": None
        }

        try:
            res = requests.post(url, headers=headers, json=data, timeout=20)
            j = res.json()

            # =========================
            # FIX LẤY MESSAGE CHUẨN
            # =========================
            msg = (
                j.get("message")
                or j.get("skip", {}).get("msg")
                or j.get("report", {}).get("msg")
                or j.get("error")
                or "NO_MESSAGE"
            )

            success = j.get("success")
            status = j.get("status")

            # print(f"status: {status} | success: {success} | skip: {msg}")


            return {
                "success": success,
                "status": status,
                "message": msg,
                "raw": j
            }

        except Exception as e:
            # print("❌ lỗi:", e)
            return {
                "success": False,
                "message": str(e)
            }
    def verify_account(self, object_id):
        url = "https://gateway.golike.net/api/fb-account/verify-account"

        headers = {
            "authorization": f"{self.token}",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://app.golike.net",
            "user-agent": "Mozilla/5.0"
        }

        payload = {
            "object_id": object_id
        }

        res = requests.post(url, headers=headers, json=payload)

        try:
            data = res.json()
        except:
            return {"success": False, "error": "invalid json"}

        print(data)              
def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string             
class facebookDapi(object):
    def __init__(self, cookie, proxy=None, page_id=None):
        try:
            self.lsd = ''
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.actor_id = page_id if page_id else self.cookie.split('c_user=')[1].split(';')[0]
            self.user_id = self.actor_id
            self.proxies = None
            self.headers = {
                'authority': 'www.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'cookie': self.cookie,
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            if proxy:
                try:
                    # ✅ nếu proxy là dict thì dùng luôn
                    if isinstance(proxy, dict):
                        self.proxies = proxy

                    # ✅ nếu là string thì parse
                    elif isinstance(proxy, str):
                        proxy_parts = proxy.strip().split(':')

                        if len(proxy_parts) == 4:
                            host, port, user, password = proxy_parts
                            self.proxies = {
                                'http': f'http://{user}:{password}@{host}:{port}',
                                'https': f'http://{user}:{password}@{host}:{port}'
                            }
                        elif len(proxy_parts) == 2:
                            host, port = proxy_parts
                            self.proxies = {
                                'http': f'http://{host}:{port}',
                                'https': f'http://{host}:{port}'
                            }

                except Exception as e:
                    print(f"Lỗi khởi tạo proxy: {str(e)}")
                    self.proxies = None
            url = requests.get(f'https://www.facebook.com/{self.actor_id}', headers=self.headers, proxies=self.proxies).url
            response = requests.get(url, headers=self.headers, proxies=self.proxies).text
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall(r'jazoest=(.*?)\"', response)[0]
                self.lsd += re.findall(r'\["LSD",\[\],\{"token":"(.*?)"\}', response)[0]
        except:
            pass
    def REACTION(self,REACTION : str,Id_post : str, doc_id : str = 'null'):
        pass
        if not isinstance(REACTION, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(Id_post, str):
            return {"success": False, "error": "Value erorr"}
        if not isinstance(doc_id, str):
            return {"success": False, "error": "Value erorr"}
        try:
            self.login()
            if not self.ready:
                return {"success": False, "error": "Not logged in"}
            payload = self.payload_builder.build_REACTION(REACTION,Id_post, doc_id )
            if 'err' in payload and payload['err']:
                return payload
        
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.header, data=payload)
            feedback_get_id = response.json().get('data', {}).get('feedback_react', {})
            if response.status_code == 200:
                if feedback_get_id : 
                    feedback_get_id_1 = feedback_get_id.get('feedback',{})
                    feedback_id = feedback_get_id_1.get('id')
                    reaction_count = feedback_get_id_1.get('i18n_reaction_count')
                    return {"success": True, "error" : None , "feedback_id" : str(feedback_id), "reaction_count" : str(reaction_count)}
                else :
                    
                    return {"success": False, "error" : str(response.json()) }
           
            else:
                return {"success": False, "error" : str(response.status_code)}
           
        except Exception as e:
             return {"success": False, "error": str(e)}    
    def checkLiveUID(uid, proxy=None):
        try:
            url = f'https://graph2.facebook.com/v3.3/{uid}/picture?redirect=0'
            headers = {
                'accept': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            proxies = None
            if proxy:
                try:
                    proxy_parts = proxy.strip().split(':')
                    if len(proxy_parts) == 4:
                        host, port, user, password = proxy_parts
                        proxy_url = f'http://{user}:{password}@{host}:{port}'
                    elif len(proxy_parts) == 2:
                        host, port = proxy_parts
                        proxy_url = f'http://{host}:{port}'
                    else:
                        proxy_url = None
                    if proxy_url:
                        proxies = {
                            'http': proxy_url,
                            'https': proxy_url
                        }
                except:
                    proxies = None
            response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
            if response.status_code != 200:
                return {'error': 'Error'}
            data = response.json()
            if 'data' in data and 'height' or 'is_silhouette' in data['data']:
                return {'success': True}
            else:
                return {'error': 'Die'}
        except:
            return {'error': 'Request failed'}
    def checkObject(self, contentID, raw=False):
        if raw:
            try:
                url = f'https://www.facebook.com/{contentID}/'
                response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=15)
                html = response.text

                if 'id="login_form"' in html or "signup" in html.lower():
                    return {"error": "Cookie die"}
                if '"initialRouteInfo"' in html:
                    block = re.search(r'"props":\s*{([^}]+)}', html)
                    if block:
                        t = re.search(r'"title":\s*"([^"]+)"', block.group(1))
                        if t:
                            return {"error": t.group(1)}
                if '"isAdminViewingDeactivatedProfile":null' in html:
                    return {'error': f'Không tìm thấy nội dung'}
                return {'success': True}
            except Exception as e:
                return {'error': f'Check failed: {e}'}
        else:
            try:
                if '/' in contentID:
                    contentID = contentID.split('/')[-1]               
                api_url = f"https://ffb.vn/api/tool/get-id-fb?idfb=https://facebook.com/{contentID}"
                r = requests.get(api_url, timeout=15)
                js = r.json()
                error_value = js.get("error")
                if error_value is None or error_value == 0:
                    real_id = js.get("id")
                    if real_id:
                        return {"success": True}
                    else:
                        return {"error": "Không tìm thấy ID"}
                else:
                    return {"error": f"API error: {error_value}"}
            except Exception as e:
                return {"error": f"{e}"}
    def checkCookie(self):
        try:
            print(f'Đang kiểm tra cookie: {self.actor_id}', end='\r')
            url = requests.get(f'https://www.facebook.com/{self.actor_id}', headers=self.headers, proxies=self.proxies, timeout=30).url
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=30)
            if response.status_code != 200:
                print(' ' * 60, end='\r')
                return {'error': f'HTTP Status: {response.status_code}'}
            html = response.text
            print(' ' * 60, end='\r')
            if "828281030927956" in html:
                return {'error': '[956] Checkpoint'}
            elif "1501092823525282" in html:
                return {'error': '[282] Checkpoint'}
            elif "601051028565049" in html:
                return {'error': 'Account blocked (spam)'}
            if 'id="login_form"' in html or "signup" in html.lower():
                return {"error": "Cookie die"}
            if 'checkpoint' in response.url or 'two_factor_authentication' in html or 'id="checkpointSubmitButton"' in html:
                return {'error': '2FA'}
            if 'log in with another device to unlock your account' in html or "We locked your account" in html:
                return {"error": "[956] Checkpoint"}
            user_id = None
            name = None
            try:
                data_split = html.split('"CurrentUserInitialData",[],{')
                if len(data_split) > 1:
                    json_data_raw = "{" + data_split[1].split("},")[0] + "}"
                    parsed_data = json.loads(json_data_raw)
                    user_id = parsed_data.get("USER_ID", "0")
                    name = parsed_data.get("NAME", "")
                    if user_id != "0" and name != "":
                        return {
                            'success': True,
                            'id': user_id,
                            'name': name
                        }
            except:
                pass
            patterns = [
                (r'aria-label="([^"]+)&#x27;s Timeline".*?class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xc5r6h4 xqeqjp1 x1phubyo x13fuv20 x18b5jzi x1q0q8m5 x1t7ytsu x972fbf x10w94by x1qhh985 x14e42zd x9f619 x1ypdohk xdl72j9 x2lah0s x3ct3a4 xdj266r xat24cr x1lziwak x2lwn1j xeuugli xexx8yu xyri2b x18d9i69 x1c1uobl x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1fmog5m xu25z0z x140muxe xo1y3bh x1q0g3np x87ps6o x1lku1pv x1a2a7pz x78zum5 x1xegmmw"', None, 1),
                (r'"id":"(\d+)","name":"([^"]+)","__isEntity":"User"', 1, 2),
                (r'"profile_user":\{"name":"([^"]+)"', None, 1),
                (r'"data":\{"name":"([^"]+)","gender"', None, 1),
                (r'"ACCOUNT_ID":"(\d+)","USER_ID":"(\d+)","NAME":"([^"]+)"', 2, 3),
            ]
            for pattern, uid_group, name_group in patterns:
                match = re.search(pattern, html)
                if match:
                    if uid_group:
                        user_id = match.group(uid_group)
                    name = match.group(name_group)
                    try:
                        name = name.encode('utf-8').decode('unicode_escape')
                    except:
                        pass
                    if not user_id:
                        user_id = self.actor_id
                    return {
                        'success': True,
                        'id': user_id,
                        'name': name
                    }
            return {'error': 'Đăng nhập thất bại'}
        except Exception as e:
            return {'error': str(e)}
    def getAccessToken(self):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'cookie': self.cookie
            }
            resp = requests.get(
                'https://business.facebook.com/content_management',
                headers=self.headers,
                proxies=self.proxies,
                timeout=10
            )
            text = resp.text
            key = '"accessToken":"'
            tokens = []
            pos = 0
            while True:
                start = text.find(key, pos)
                if start == -1:
                    break
                start_val = start + len(key)
                end_val = text.find('"', start_val)
                if end_val == -1:
                    break
                value = text[start_val:end_val]
                if value.startswith("EAAG"):
                    tokens.append(value)
                pos = end_val + 1
            if tokens:
                access_token = max(tokens, key=len)
                if self.checkAccessToken(access_token):
                    return access_token
            return None
        except:
            return None
    def getPageAccessToken(self, delegate_page_id, user_token):
        try:
            url = f'https://graph.facebook.com/me/accounts?access_token={user_token}'
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            result = response.json()
            if 'error' in result:
                return None
            for page in result.get('data', []):
                if page.get('id') == str(delegate_page_id):
                    page_token = page.get('access_token')
                    if page_token:
                        return page_token
            return None
        except:
            return None
    def checkAccessToken(self, token):
        try:
            url = f'https://graph.facebook.com/me?access_token={token}'
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            result = response.json()
            if 'error' in result:
                return False
            if result.get('id'):
                return True
            return False
        except:
            return False
    def getPrivacyWriteID(self, postID):
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'cookie': self.cookie,
                'dpr': '1',
                'priority': 'u=0, i',
                'referer': 'https://www.facebook.com/',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                'sec-ch-ua-full-version-list': '"Chromium";v="142.0.7444.163", "Google Chrome";v="142.0.7444.163", "Not_A Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'viewport-width': '752'
            }
            url = f'https://www.facebook.com/{postID}'
            resp = requests.get(url, headers=headers, proxies=self.proxies, timeout=10)
            response = resp.text
            privacy_write_id = None
            matches = re.findall(r'"privacy_write_id"\s*:\s*"([^"]+)"', response)
            if matches:
                privacy_write_id = matches[0]
            else:
                if 'Sorry, something went wrong' in response or '<title>Error</title>' in response:
                    return {'privacy_write_id': None, 'label': None}
            label = None
            label_matches = re.findall(r'"label":"(Public|Only me|Friends)', response)
            if label_matches:
                label = label_matches[0]
            else:
                alt_label_matches = re.findall(r'"privacy_option_name":"([^"]+)"', response)
                if alt_label_matches:
                    label = alt_label_matches[0]
            result = {
                'privacy_write_id': privacy_write_id,
                'label': label
            }
            return result
        except Exception as e:
            return {
                'privacy_write_id': None,
                'label': None
            }
    def changePrivacy(self, postID):
        try:
            privacy_info = self.getPrivacyWriteID(postID)
            if not privacy_info['privacy_write_id']:
                return {'success': False, 'error': 'Không tìm thấy ID riêng tư'}
            if privacy_info['label'] == 'Public':
                return {'success': True, 'already_public': True}
            url = "https://www.facebook.com/api/graphql/"
            headers = {
                'accept': '*/*',
                'accept-encoding': 'identity',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': self.cookie,
                'origin': 'https://www.facebook.com',
                'priority': 'u=1, i',
                'referer': 'https://www.facebook.com/',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                'sec-ch-ua-full-version-list': '"Chromium";v="142.0.7444.163", "Google Chrome";v="142.0.7444.163", "Not_A Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'x-asbd-id': '359341',
                'x-fb-friendly-name': 'CometPrivacySelectorSavePrivacyMutation',
                'x-fb-lsd': self.lsd
            }
            payload = {
                'av': self.actor_id,
                '__aaid': '0',
                '__user': self.actor_id,
                '__a': '1',
                '__req': '1m',
                '__hs': '20406.HYP:comet_pkg.2.1...0',
                'dpr': '1',
                '__comet_req': '15',
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'lsd': self.lsd,
                '__spin_r': '1029895235',
                '__spin_b': 'trunk',
                '__spin_t': '1763128405',
                '__crn': 'comet.fbweb.CometProfileTimelineListViewRoute',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometPrivacySelectorSavePrivacyMutation',
                'server_timestamps': 'true',
                'variables': json.dumps({
                    "input": {
                        "privacy_mutation_token": None,
                        "privacy_row_input": {
                            "allow": [],
                            "base_state": "EVERYONE",
                            "deny": [],
                            "tag_expansion_state": "UNSPECIFIED"
                        },
                        "privacy_write_id": privacy_info['privacy_write_id'],
                        "render_location": "COMET_STREAM",
                        "actor_id": self.user_id,
                        "client_mutation_id": "1"
                    },
                    "privacySelectorRenderLocation": "COMET_STREAM",
                    "scale": 1,
                    "storyRenderLocation": "timeline",
                    "tags": None,
                    "__relay_internal__pv__CometUFIShareActionMigrationrelayprovider": True
                }),
                'doc_id': '24757748563916145'
            }
            response = requests.post(url, headers=headers, data=payload, proxies=self.proxies, timeout=10)
            response_text = response.text
            if response_text.startswith('for (;;);'):
                response_text = response_text[9:]
            if response_text.strip():
                response_json = json.loads(response_text)
                if 'data' in response_json and 'privacy_selector_save' in response_json['data']:
                    return {'success': True, 'already_public': False}
                else:
                    return {'success': False, 'error': 'phản hồi không hợp lệ'}
            else:
                return {'success': False, 'error': 'không có phản hồi'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    def reaction(self, id, type):
        if str(id).startswith("S:"):
            story_id = str(id)[2:]  # Bỏ prefix "S:"
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.facebook.com',
                'priority': 'u=1, i',
                'referer': 'https://www.facebook.com/',
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'x-fb-friendly-name': 'useStoriesSendReplyMutation',
                'x-fb-lsd': self.lsd,
                'cookie': self.cookie
            }
            json_data = {
                'av': str(self.actor_id),
                '__user': str(self.actor_id),
                'fb_dtsg': self.fb_dtsg,
                'jazoest': str(self.jazoest),
                'lsd': self.lsd,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'useStoriesSendReplyMutation',
                'variables': '{"input":{"attribution_id_v2":"StoriesCometSuspenseRoot.react,comet.stories.viewer,via_cold_start,'+str(int(time.time()*1000))+',33592,,,","lightweight_reaction_actions":{"offsets":[0],"reaction":"❤️"},"message":"❤️","story_id":"'+str(story_id)+'","story_reply_type":"LIGHT_WEIGHT","actor_id":"'+str(self.actor_id)+'","client_mutation_id":"2"}}',
                'server_timestamps': 'true',
                'doc_id': '9697491553691692',
            }
            try:
                response = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=json_data, proxies=self.proxies, timeout=15)
                response_json = response.json()
                if response_json.get('extensions', {}).get('is_final') == True:
                    return True
                else:
                    return {'error': 'Failed', 'response': response.text}
            except Exception as e:
                return {'error': str(e)}
        elif str(id).startswith("P:"):
            post_id = str(id)[2:]  # Bỏ prefix "P:"
            react_list = {
                "LIKE": "1635855486666999",
                "LOVE": "1678524932434102",
                "CARE": "613557422527858",
                "HAHA": "115940658764963",
                "WOW": "478547315650144",
                "SAD": "908563459236466",
                "ANGRY": "444813342392137"
            }
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.facebook.com',
                'priority': 'u=1, i',
                'referer': 'https://www.facebook.com/'+str(post_id),
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'x-fb-friendly-name': 'CometUFIFeedbackReactMutation',
                'x-fb-lsd': self.lsd,
                'cookie': self.cookie,
            }
            json_data = {
                'av': str(self.actor_id),
                '__user': str(self.actor_id),
                'fb_dtsg': self.fb_dtsg,
                'jazoest': str(self.jazoest),
                'lsd': str(self.lsd),
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
                'variables': '{"input":{"attribution_id_v2":"CometSinglePostDialogRoot.react,comet.post.single_dialog,via_cold_start,'+str(int(time.time()*1000))+',893597,,,","feedback_id":"'+encode_to_base64(str('feedback:'+post_id))+'","feedback_reaction_id":"'+str(react_list.get(type.upper()))+'","feedback_source":"OBJECT","is_tracking_encrypted":true,"tracking":["AZWEqXNx7ELYfHNA7b4CrfdPexzmIf2rUloFtOZ9zOxrcEuXq9Nr8cAdc1kP5DWdKx-DdpkffT5hoGfKYfh0Jm8VlJztxP7elRZBQe5FqkP58YxifFUwdqGzQnJPfhGupHYBjoq5I5zRHXPrEeuJk6lZPblpsrYQTO1aDBDb8UcDpW8F82ROTRSaXpL-T0gnE3GyKCzqqN0x99CSBp1lCZQj8291oXhMoeESvV__sBVqPWiELtFIWvZFioWhqpoAe_Em15uPs4EZgWgQmQ-LfgOMAOUG0TOb6wDVO75_PyQ4b8uTdDWVSEbMPTCglXWn5PJzqqN4iQzyEKVe8sk708ldiDug7SlNS7Bx0LknC7p_ihIfVQqWLQpLYK6h4JWZle-ugySqzonCzb6ay09yrsvupxPUGp-EDKhjyEURONdtNuP-Fl3Oi1emIy61-rqISLQc-jp3vzvnIIk7r_oA1MKT065zyX-syapAs-4xnA_12Un5wQAgwu5sP9UmJ8ycf4h1xBPGDmC4ZkaMWR_moqpx1k2Wy4IbdcHNMvGbkkqu12sgHWWznxVfZzrzonXKLPBVW9Y3tlQImU9KBheHGL_ADG_8D-zj2S9JG2y7OnxiZNVAUb1yGrVVrJFnsWNPISRJJMZEKiYXgTaHVbZBX6CdCrA7gO25-fFBvVfxp2Do3M_YKDc5Ttq1BeiZgPCKogeTkSQt1B67Kq7FTpBYJ05uEWLpHpk1jYLH8ppQQpSEasmmKKYj9dg7PqbHPMUkeyBtL69_HkdxtVhDgkNzh1JerLPokIkdGkUv0RALcahWQK4nR8RRU2IAFMQEp-FsNk_VKs_mTnZQmlmSnzPDymkbGLc0S1hIlm9FdBTQ59--zU4cJdOGnECzfZq4B5YKxqxs0ijrcY6T-AOn4_UuwioY"],"session_id":"'+str(uuid.uuid4())+'","actor_id":"'+str(self.actor_id)+'","client_mutation_id":"1"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}',
                'server_timestamps': 'true',
                'doc_id': '24034997962776771',
            }
            try:
                response = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=json_data, proxies=self.proxies, timeout=15)
                if '{"data":{"feedback_react":{"feedback":{"id":' in response.text:
                    return True
                else:
                    return {'error': 'Failed', 'response': response.text}
            except Exception as e:
                return {'error': str(e)}
        else:
            reac = {
                "LIKE": "1635855486666999",
                "LOVE": "1678524932434102",
                "CARE": "613557422527858",
                "HAHA": "115940658764963",
                "WOW": "478547315650144",
                "SAD": "908563459236466",
                "ANGRY": "444813342392137"
            }
            idreac = reac.get(type.upper())
            data = {
                'av': self.actor_id,
                '__usid': r'6-Tsfgotwhb2nus:Psfgosvgerpwk:0-Asfgotw11gc1if-RV=6:F=',
                '__aaid': '0',
                '__user': self.actor_id,
                '__a': '1',
                '__req': '2c',
                '__hs': '19896.HYP:comet_pkg.2.1..2.1',
                'dpr': '1',
                '__ccg': 'EXCELLENT',
                '__rev': '1014402108',
                '__s': '5vdtpn:wbz2hc:8r67q5',
                '__hsi': '7383159623287270781',
                '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C17xt3odE98K361twYwJyE24wJwpUe8hwaG1sw9u0LVEtwMw65xO2OU7m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwqo31wiE567Udo5qfK0zEkxe2GewyDwkUe9obrwKxm5oe8464-5pUfEdK261eBx_wHwdG7FoarCwLyES0Io88cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13whEeE4WVU-4EdrxG1fy8bUaU','__csr': 'gug_2A4A8gkqTf2Ih6RFnbk9mBqaBaTs8_tntineDdSyWqiGRYCiPi_SJuLCGcHBaiQXtLpXsyjIymm8oFJswG8CSGGLzAq8AiWZ6VGDgyQiiTBKU-8GczE9USmi4A9DBABHgWEK3K9y9prxaEa9KqQV8qUlxW22u4EnznDxSewLxq3W2K16BxiE5VqwbW1dz8qwCwjoeEvwaKVU6q0yo5a2i58aE7W0CE5O0fdw1jim0dNw7ewPBG0688025ew0bki0cow3c8C05Vo0aNF40BU0rmU3LDwaO06hU06RG6U1g82Bw0Gxw6Gw',
                '__comet_req': '15',
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'lsd': self.lsd,
                '__spin_r': '1014402108',
                '__spin_b': 'trunk',
                '__spin_t': '1719025807',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
                'variables': fr'{{"input":{{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,{int(time.time()*1000)},322693,4748854339,,","feedback_id":"{encode_to_base64("feedback:"+str(id))}","feedback_reaction_id":"{idreac}","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"tracking":["AZWUDdylhKB7Q-Esd2HQq9i7j4CmKRfjJP03XBxVNfpztKO0WSnXmh5gtIcplhFxZdk33kQBTHSXLNH-zJaEXFlMxQOu_JG98LVXCvCqk1XLyQqGKuL_dCYK7qSwJmt89TDw1KPpL-BPxB9qLIil1D_4Thuoa4XMgovMVLAXncnXCsoQvAnchMg6ksQOIEX3CqRCqIIKd47O7F7PYR1TkMNbeeSccW83SEUmtuyO5Jc_wiY0ZrrPejfiJeLgtk3snxyTd-JXW1nvjBRjfbLySxmh69u-N_cuDwvqp7A1QwK5pgV49vJlHP63g4do1q6D6kQmTWtBY7iA-beU44knFS7aCLNiq1aGN9Hhg0QTIYJ9rXXEeHbUuAPSK419ieoaj4rb_4lA-Wdaz3oWiWwH0EIzGs0Zj3srHRqfR94oe4PbJ6gz5f64k0kQ2QRWReCO5kpQeiAd1f25oP9yiH_MbpTcfxMr-z83luvUWMF6K0-A-NXEuF5AiCLkWDapNyRwpuGMs8FIdUJmPXF9TGe3wslF5sZRVTKAWRdFMVAsUn-lFT8tVAZVvd4UtScTnmxc1YOArpHD-_Lzt7NDdbuPQWQohqkGVlQVLMoJNZnF_oRLL8je6-ra17lJ8inQPICnw7GP-ne_3A03eT4zA6YsxCC3eIhQK-xyodjfm1j0cMvydXhB89fjTcuz0Uoy0oPyfstl7Sm-AUoGugNch3Mz2jQAXo0E_FX4mbkMYX2WUBW2XSNxssYZYaRXC4FUIrQoVhAJbxU6lomRQIPY8aCS0Ge9iUk8nHq4YZzJgmB7VnFRUd8Oe1sSSiIUWpMNVBONuCIT9Wjipt1lxWEs4KjlHk-SRaEZc_eX4mLwS0RcycI8eXg6kzw2WOlPvGDWalTaMryy6QdJLjoqwidHO21JSbAWPqrBzQAEcoSau_UHC6soSO9UgcBQqdAKBfJbdMhBkmxSwVoxJR_puqsTfuCT6Aa_gFixolGrbgxx5h2-XAARx4SbGplK5kWMw27FpMvgpctU248HpEQ7zGJRTJylE84EWcVHMlVm0pGZb8tlrZSQQme6zxPWbzoQv3xY8CsH4UDu1gBhmWe_wL6KwZJxj3wRrlle54cqhzStoGL5JQwMGaxdwITRusdKgmwwEQJxxH63GvPwqL9oRMvIaHyGfKegOVyG2HMyxmiQmtb5EtaFd6n3JjMCBF74Kcn33TJhQ1yjHoltdO_tKqnj0nPVgRGfN-kdJA7G6HZFvz6j82WfKmzi1lgpUcoZ5T8Fwpx-yyBHV0J4sGF0qR4uBYNcTGkFtbD0tZnUxfy_POfmf8E3phVJrS__XIvnlB5c6yvyGGdYvafQkszlRrTAzDu9pH6TZo1K3Jc1a-wfPWZJ3uBJ_cku-YeTj8piEmR-cMeyWTJR7InVB2IFZx2AoyElAFbMuPVZVp64RgC3ugiyC1nY7HycH2T3POGARB6wP4RFXybScGN4OGwM8e3W2p-Za1BTR09lHRlzeukops0DSBUkhr9GrgMZaw7eAsztGlIXZ_4"],"session_id":"{uuid.uuid4()}","actor_id":"{self.actor_id}","client_mutation_id":"3"}},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}}',
                'server_timestamps': 'true',
                'doc_id': '7047198228715224',
            }
            try:
                response = requests.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data, proxies=self.proxies, timeout=15)
                if '{"data":{"feedback_react":{"feedback":{"id":' in response.text:
                    return True
                else:
                    return {'error': 'Failed', 'response': response.text}
            except Exception as e:
                return {'error': f'Proxy/Network error: {str(e)}'} 
    def reactionComment(self, id, type):
        reac = {
            "LIKE": "1635855486666999",
            "LOVE": "1678524932434102",
            "CARE": "613557422527858",
            "HAHA": "115940658764963",
            "WOW": "478547315650144",
            "SAD": "908563459236466",
            "ANGRY": "444813342392137"
        }
        g_now = datetime.now()
        d = g_now.strftime("%Y-%m-%d %H:%M:%S.%f")
        datetime_object = datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f")
        timestamp = str(datetime_object.timestamp())
        starttime = timestamp.replace('.', '')
        id_reac = reac.get(type)
        data = {
            'av': self.actor_id, 
            '__aaid': '0', 
            '__user': self.actor_id, 
            '__a': '1', 
            '__req': '1a', 
            '__hs': '19906.HYP:comet_pkg.2.1..2.1', 
            'dpr': '1', 
            '__ccg': 'GOOD', 
            '__rev': '1014619389', 
            '__s': 'z5ciff:vre7af:23swxc', 
            '__hsi': '7387045920424178191', 
            '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C1vgS3q2ibwyzE2qwJyE24wJwkEkwUx60GE5O0BU2_CxS320om78-221Rwwwqo462mcwfG12wOx62G5Usw9m1YwBgK7o6C2O0B84G1hx-3m1mzXw8W58jwGzEaE5e3ym2SUbElxm3y11xfxmu3W3rwxwjFovUaU3VBwFKq2-azo2NwwwOg2cwMwhEkxebwHwNxe6Uak0zU8oC1hxB0qo4e16wWwjHDzUiwRK6E4-8wLwHw', 
            '__csr': 'gJ0AH5n4n4PhcQW4Oh4JFsIH4f5ji9iWuzqSltFlETn_trnbH_YIJX9iWiAiQBpeht9uYyhrvOOaiSV9CKmriyF4EzjBGh4XRqy8O4Z4HGypAaDAG8DzE-iKii5bUGaiXyocA22iayUOUG9BKUkxe2vBBxe5898S5k48fogxqQU9oO1bwiU9FpEowOBwYwLCw86u2y0Eo885-1uwFwOwpU1jo7-0IU108iw8i0kq0bVw6gBxa4E1g83tw0_yBw2hE012EoG0uG0gh068w23Q0dlw0wKw68Aw0huU0a7VU0jkw0E-w8W0cPK6U', 
            '__comet_req': '15', 
            'fb_dtsg': self.fb_dtsg, 
            'jazoest': self.jazoest, 
            'lsd': self.lsd, 
            '__spin_r': '1014619389', 
            '__spin_b': 'trunk', 
            '__spin_t': '1719930656', 
            'fb_api_caller_class': 'RelayModern', 
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation', 
            'variables': '{"input":{"attribution_id_v2":"CometVideoHomeNewPermalinkRoot.react,comet.watch.injection,via_cold_start,1719930662698,975645,2392950137,,","feedback_id":"'+encode_to_base64("feedback:"+str(id))+'","feedback_reaction_id":"'+id_reac+'","feedback_source":"TAHOE","is_tracking_encrypted":true,"tracking":[],"session_id":"'+str(uuid.uuid4())+'","downstream_share_session_id":"'+str(uuid.uuid4())+'","downstream_share_session_origin_uri":"https://fb.watch/t3OatrTuqv/?mibextid=Nif5oz","downstream_share_sessionStartTime":"'+starttime+'","actor_id":"'+self.actor_id+'","client_mutation_id":"1"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}', 
            'server_timestamps': 'true',
            'doc_id': '7616998081714004',
        }
        try:
            response = requests.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data, proxies=self.proxies, timeout=15)
            if '{"data":{"feedback_react":{"feedback":{"id":' in response.text:
                return True
            else:
                return {'error': 'Failed', 'response': response.text}
        except Exception as e:
            return {'error': f'Proxy/Network error: {str(e)}'}
    def share(self, id, token=None):
        if not token:
            data = {
                'av': self.actor_id,
                '__usid': r'6-Tsftw3x1vqj8dz:Psftw2g2c595x:0-Asftw3x1etit7l-RV=6:F=',
                '__aaid': '0',
                '__user': self.actor_id,
                '__a': '1',
                '__req': '1o',
                '__hs': '19901.HYP:comet_pkg.2.1..2.1',
                'dpr': '1',
                '__ccg': 'EXCELLENT',
                '__rev': '1014511729',
                '__s': '8zktjb:5quia4:fu1x9q',
                '__hsi': '7384980750065440159',
                '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C17xt3odE98K360CEboG0x8bo6u3y4o2Gwn82nwb-q7oc81xoswMwto886C11wBz83WwgEcEhwGxu782lwv89kbxS1Fwc61awkovwRwlE-U2exi4UaEW2G1jwUBwJK2W5olwUwgojUlDw-wSU8o4Wm7-2K0-poarCwLyES0Io88cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13whEeE4WVU-4EdrxG1fy8bUaU',
                '__csr': 'gdk8MPs4dNYQYp4iOSD9sG2fZqN79mKHYBH4qrNP5bifl8IyAF-CDQGFdBdlTmeimHGOWJKhCKRWDLjGmV94uVpprh6FaDD_GcG5F4ECVqgCqhqRAKhd2oGAUBzaUCibGVHy9EFeayEjCxim598oxmmCETxObKuuUyfzF8411e2e7VHyq-dG8AK4oW4ogK69XzEy7U4aFQ4EdE426UKdxm7E98sG15Cw8Oi1awgUaolwvUO8wrU3ewNwt9UOvwko16o1z81uo1gA0cww1pHxGQE2Kw0sv80Ii6E03c4U9olw1N21Cw1eu05rE1oUmxiew0iIU0e5k0m-02jW1RyU2pwPw3uU0u3w4wAo0Xi0Bk',
                '__comet_req': '15',
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'lsd': self.lsd,
                '__spin_r': '1014511729',
                '__spin_b': 'trunk',
                '__spin_t': '1719449821',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'ComposerStoryCreateMutation',
                'variables': '{"input":{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"'+str(uuid.uuid4())+'_FEED","source":"WWW","attachments":[{"link":{"share_scrape_data":"{\\"share_type\\":22,\\"share_params\\":['+id+']}"}}],"reshare_original_post":"RESHARE_ORIGINAL_POST","audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"is_tracking_encrypted":true,"tracking":["AZWWGipYJ1gf83pZebtJYQQ-iWKc5VZxS4JuOcGWLeB-goMh2k74R1JxqgvUTbDVNs-xTyTpCI4vQw_Y9mFCaX-tIEMg2TfN_GKk-PnqI4xMhaignTkV5113HU-3PLFG27m-EEseUfuGXrNitybNZF1fKNtPcboF6IvxizZa5CUGXNVqLISUtAWXNS9Lq-G2ECnfWPtmKGebm2-YKyfMUH1p8xKNDxOcnMmMJcBBZkUEpjVzqvUTSt52Xyp0NETTPTVW4zHpkByOboAqZj12UuYSsG3GEhafpt91ThFhs7UTtqN7F29UsSW2ikIjTgFPy8cOddclinOtUwaoMaFk2OspLF3J9cwr7wPsZ9CpQxU21mcFHxqpz7vZuGrjWqepKQhWX_ZzmHv0LR8K07ZJLu8yl51iv-Ram7er9lKfWDtQsuNeLqbzEOQo0UlRNexaV0V2m8fYke8ubw3kNeR5XsRYiyr958OFwNgZ3RNfy-mNnO9P-4TFEF12NmNNEm4N6h0_DRZ-g74n-X2nGwx9emPv4wuy9kvQGeoCqc636BfKRE-51w2GFSrHAsOUJJ1dDryxZsxQOEGep3HGrVp_rTsVv7Vk3JxKxlzqt3hnBGDgi6suTZnJw69poVOIz6TPCTthRhj7XUu4heyKBSIeHsjBRC2_s3NwuZ4kKNCQ2JkVuBXz_hsRhDmbAnBi6WUFIJhLHO_bGgKbEASuU4vtj4FNKo_G8p-J1kYmCo0Pi72Csi3EikuocfjHFwfSD3cCbetr3V8Yp6OmSGkqX63FkSqzBoAcHFeD-iyCAkn0UJGqU-0o670ZoR-twkUDcSJPXDN2NYQfqiyb9ZknZ7j04w1ZfAyaE7NCiCc-lDt1ic79XyHunjOyLStgXIW30J4OEw_hAn86LlRHbYVhi-zBBTZWWnEl9piuUz0qtnN-qEd002DjNYaMy0aDAbL9oOYDdN8mHvnXq1aKove9I4Jy0WtlxeN8279ayz7NdDZZ9LrajY_YxIJJqdZtJIuRYTunEeDsFrORpu3RYRbFwpGnQbHeSLH1YvwOyOJRXhYYmVLJEGD2N9r5wkPbgbx2HoWsGjWj_DpkEAyg59eBJy4RYPJHvOsetBQABEWmGI7nhUDYTPdhrzVxqB_g4fQ9JkPzIbEhcoEZjmspGZcR4z4JxUDJCNdAz2aK4lR4P5WTkLtj2uXMDD_nzbl8r_DMcj23bjPiSe0Fubu-VIzjwr7JgPNyQ1FYhp5u4lpqkkBkGtfyAaUjCgFhg4FW-H3d3vPVMO--GxbhK9kN0QAcOE3ZqQR2dRz6NbhcvTyNfDxy0dFTRw-f-vxn04gjJB5ZEG3WfSzQv0VbqDYm6-NFYAzIxbDLoiCu34WAa2lckx5qxncXBhQj6Fro2gXGPXo4d32DvqQg7_RHQ-SF_WLqdxRCXF91NIqxYmFZsOJAuQ5m6TafzuNnQoJB3OQFoknv8Uy5O4FKuwazh1rvLrsj-1QEMi3sTrr9KxJkZy9EKXs92ndlb3edgfycLOffTil-gW2BvxeNiMQzqF1xJqFBKHDyatgwpXDX81HDwxkuMEaGPREIeQLuOlBJrL_20RD1e4Gu4tjQD8vRsb29UNG60DqpDvc-H4Z2oxeppm0KIwQNaCTtGUxxmvT807fXMnuVEf5QI5qTx9YRJh56GiWLoHC_zPMhoikMbAybIVWh9HtVgZGgImDmz0l9P4LgtpKNnKbQj_2ZKn2ZhOYKZLdt1P2Jq2Z2z76MtbRQTrpZpFb14zWVnh1LFCSFPAB7sqC1-u-KQOf2_SjEecztPccso8xZB2nkhLetyPn9aFuO-J_LCZydQeiroXx4Z8NxhDpbLoOpw2MbRCVB_TxfnLGNn1QD0To9TTChxK5AHNRRLDaj3xK1e0jd37uSmHTkT6QJVHFHEYMVLBcuV1MQcoy0wsvc1sRb",null],"logging":{"composer_session_id":"'+str(uuid.uuid4())+'"},"navigation_data":{"attribution_id_v2":"FeedsCometRoot.react,comet.most_recent_feed,tap_bookmark,1719641912186,189404,608920319153834,,"},"event_share_metadata":{"surface":"newsfeed"},"actor_id":"'+self.actor_id+'","client_mutation_id":"3"},"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":false,"renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":true,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometIsAdaptiveUFIEnabledrelayprovider":true,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__IncludeCommentWithAttachmentrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__StoriesRingrelayprovider":false,"__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider":false}',
                'server_timestamps': 'true',
                'doc_id': '8167261726632010'
            }
            try:
                response = requests.post("https://www.facebook.com/api/graphql/",headers=self.headers, data=data, proxies=self.proxies, timeout=15)
                if '"errors"' not in response.text:
                    return True
                else:
                    return {'error': 'Failed', 'response': response.text}
            except Exception as e:
                return {'error': f'Proxy/Network error: {str(e)}'}
        try:
            url = f'https://graph.facebook.com/v21.0/me/feed'
            params = {
                'link': f'https://www.facebook.com/{id}',
                'privacy': '{"value":"EVERYONE"}',
                'access_token': token
            }
            response = requests.post(url, params=params, headers=self.headers, proxies=self.proxies, timeout=10)
            if response.status_code != 200:
                return {'error': 'failed', 'response': response.text}
            result = response.json()
            if 'id' in result:
                return {'success': True, 'postID': result['id']}
            elif 'error' in result:
                return {'error': f"{result['error'].get('message', 'Unknown')}", 'response': response.text}
            else:
                return {'error': 'No post ID in response', 'response': response.text}
        except Exception as e:
            return {'error': str(e)}
    def likePage(self, id):
        data = {
            'av': self.actor_id,
            '__aaid': '0',
            '__user': self.actor_id,
            '__a': '1',
            '__req': '1p',
            '__hs': '20404.HYP:comet_pkg.2.1...0',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1029770999',
            '__s': 'h8mjp8:76vm28:wdjefl',
            '__hsi': '7571833640484796231',
            '__dyn': '7xeUjGU5a5Q1ryaxG4Vp41twWwIxu13wFwhUngS3q2ibwNwnof8boG0x8bo6u3y4o2Gwfi0LVEtwMw6ywIK1Rwwwqo462mcwfG12wOx62G5Usw9m1YwBgK7o6C1uwoE4G17yovwRwlE-U2exi4UaEW2au1jwUBwJK14xm3y11xfxmu3W3y261eBx_wHwfC2-awLyESE2KwwwOg2cwMwhEkxebwHwKG4UrwFg2fwxyo566k1fxC13xecwBwWzUfHDzUiBG2OUqwjVqwLwHwa211wo83KwHwOyUqxG',
            '__csr': 'g4d3kpf9MiT6nf9kD5-WNs8gB2cz7HNsylij_Qx6gQWHn2biFeABmmGicR9lRqWHBJvmHiKaJ24CAHhblQi_TlF6ybGmJrHuAZ94FGK9XjqQrV6ch4iAKLAWGQeAzt1mmEC-iniCRKjj_r-p1by_yUFyuFrDDLxejBySXWVUGEyEObjJx2Qao-ubDIxaBGrCBAQteG-vKUhyWV8hyEyHKmbVpKuijGezpUGF98h-cLUOiXBzGyppEsV9Eyi7e8AgoyqzoGbwywwQm8hV89opz8CjAHCAGm59HBzHDwJxebUdQczaBhoaGXxe-58rU9VpU8ofoSi5oph8W5po5Sbxh1OFk4Ubumu2q1rzU761ACwFF0xgK3WEgx658Rwlo8omCwQwzwSxq58rxmm1Wwfh0GwaGcRwcu18U4aewiEyexrBwca781bE2lwqojwho3Yw8ebgbU6i18y8rG2KFEiK689U1bWg09sU1i-04Y87G8g1-UKjw1Jh0uA0v207tU6W2e0-o03qjwcp07twGAynSdwJgc8io1f83b80-83iV2wnE2kg1uu09Jo1F9oG0JXw3RU22o0wS1YKcwgk8ykcy8qwCw8u0d2g727o0nDwWwgy0248560aQw2v84a08Ew5Hw13u05vk0jKm0dr80r-mU1ao40Msw2Fo0oywio0hgwEwNxi5U0GRw6p82a06f8jwf65E14Uy5EcU7i08_w2zU',
            '__hsdp': 'gfx55EV1y3GFFHCqpai44csgsOF9E9EgD32C3IiMsawl8siCAwGCMxf2yIt4Et3AxyTk4RJySoAQ8gSIl4A2O117gTaNhjFh559F8IHkkGiEAgaEIy75ZPhgOSgaqiHpqDiqjINS8gF0wsxh2R2IGqey8kAg-B45iQxdPgV290jheF389A78n9d2kxoAgj2Oi7c9cQBlPapcGhFA9DgPyha6p-oqAKLQQfWAhahaRpkGcbV8CUGEiCwIBzz6BLqBEWx0gmbduizx51kxp4fyizogy94FmWsZrAKi4UsGBPat2hp8G9lBa5nwA88yXxhzEWaDjwyeAh7Bzo9y0Awzomz8Zdm32dBiw-zEmyUBXyu4pbLXgGF1s5Rhl5e-9BZ49imMIbxl5hokGJ0VG982N4ze10xNyVEy2LwYw8m64cyWx54y3110h8GUC4U5G6Enxi4QudwIBolwlE5a0VEF2E8E4S48Cu1awgp8gDOu1bF1Kdz8c8a8S2_wywRoG3SEIwgz8-9wjVUlwlU2fxaGm49K0T9oaoZpqy6eyU4a4Ey0MUzg3Rxyq0X82LwxwSw8O0xE3lDw4zwgo39w4nw8Z121Ox60a3way1lw2QU7Si0oC089w6pwe7wIwTzE3owpUe8foiw8a1mxjw70wp89Eco20weq09wwXw6iwvU1tU5-1PxR0CAw4twfa0GE1R81go2_wiE1XE20w4twnXw82',
            '__hblp': '1a54324U-1Uz84GfxZx60he74dyawgo3xwYyoaEc8uw9K69VUaE6u0OUO26aKq0EUK0Lo8oiDwwx6dyFob8bocEG7ESexy1iwDwTwJwSwhUW6U4S1Ow-wAx-36fgW1cwzwau12xR0hUfE25xCcyUkBx-12z8S4U5G2WUfUs8cKWwqo2ww825UdU624olwPho4248G0iq2a3m1awyU984-14wMw8-5qm483HwVg791a0Jovw8q0Ao2gwmU3-wkE4e0xA7o7W3uu3W0V8464E2rgiCCwywpoc8O58d82fggwem1Wxi0J82FwOwaC1JwqEsw9W1Qwv81898qw5Kwdy0E9E28wto18U1i8560Bo6u2e589Emxa0wE5q5e2e3K1vwPwcO1AwwBwNw823-0FGw4PWxu8w8-4U5-3K3i3q1Swtoeo5q9w9d1m0E8owByUiy8aEoxG3C1Fwdx07vorwZggwLwKwlE2Owfm1bw47Gi1ww57wg9o4y9BzUhw4hyU5iaK0w8O',
            '__sjsp': 'gfx55EV1y3GFFHCqpai44csgsOF9E9EgD32C3IiMsawl8siCVwyCNBOYjdqKoYiD58n7O6bqMRNdJySpEQ8gSIl4A2O117gSydApnWkhhDGOOJjmGiEx2znAEgAuXqFxpxCUC2Z0rbVV6yJehmGhC5UbCz5UK6P2mdzy0VguC6z4dghK46agG263K22QQ6k7k0ZU8k5AbwIxCh0vA9wsk1fwdBxq1Hg461Ow3No29wg4u0vm0j20ka061FE',
            '__crn': 'comet.fbweb.CometProfileTimelineListViewRoute',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            '__spin_r': '1029770999',
            '__spin_b': 'trunk',
            '__spin_t': '1762954900',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometProfilePlusLikeMutation',
            'server_timestamps': 'true',
            'variables': '{"input":{"is_tracking_encrypted":false,"page_id":"'+str(id)+'","source":null,"tracking":null,"actor_id":"'+str(self.actor_id)+'","client_mutation_id":"4"},"scale":1}',
            'doc_id': '25463905889878308',
        }
        try:
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies, timeout=15)
            if '<!DOCTYPE html>' in response.text or '<html' in response.text:
                return {'error': 'HTML_ERROR', 'response': response.text}

            if '"subscribe_status":"IS_SUBSCRIBED"' in response.text:
                return True
            else:
                return {'error': 'Failed', 'response': response.text}
        except Exception as e:
            return {'error': f'Proxy/Network error: {str(e)}'}
    def doJoinGroup(self, id):
        data = {
            'av': self.actor_id,
            '__user': self.actor_id,
            '__a': '1',
            '__dyn': '7AzHJ16U9ob8ng5K8G6EjBWo2nDwAxu13wsongS3q2ibwyzE2qwJyEiwsobo6u3y4o2Gwfi0LVEtwMw65xO321Rwwwg8a8465o-cwfG12wOKdwGxu782lwv89kbxS2218wc61axe3S1lwlE-U2exi4UaEW2G1jxS6FobrwKxm5oe8464-5pUfEe88o4Wm7-8xmcwfCm2CVEbUGdG1Fwh888cA0z8c84qifxe3u364UrwFg662S26',
            '__csr': 'gadNAIYllhsKOE8IpidFPhcIx34Omy9-O9OO8hZ_8-kAymHGAybJqGlvmWl7nWBWJ7GqaXHz7GFe9oy_KBl7h6h4KVah94QeKVHACDyryqKdF5GuXXBCgNpbJ5jjGm8yQEWrCixl6xWuiih5yo-8wAy84mq4poN0Vzbxe16whAufgO5U8UKi4Eyu4EjwGK78527o8411wgocU5u1MwSwFyU8Uf8igaElw8e9xK2GewNgy5o5m1nDwLwrokm16www8G03cy0arw0Zyw0aaC0mG0eJzl8ow2Jw6tw44w4uzo045W1UgSeg0z-07X81-E0cNo0By1Wwi8fE0lYw2h81a8gw9u',
            '__req': 'k',
            '__hs': '19363.HYP:comet_pkg.2.1.0.2.1',
            'dpr': '2',
            '__ccg': 'EXCELLENT',
            '__rev': '1006794317',
            '__s': 'gtlvj8:fxbzro:f2kk19',
            '__hsi': '7185658639628512803',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            '__aaid': '1576489885859472',
            '__spin_r': '1006794317',
            '__spin_b': 'trunk',
            '__spin_t': '1673041526',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'GroupCometJoinForumMutation',
            'variables': '{"feedType":"DISCUSSION","groupID":"'+id+'","imageMediaType":"image/x-auto","input":{"action_source":"GROUP_MALL","attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,via_cold_start,1673041528761,114928,2361831622,","group_id":"'+id+'","group_share_tracking_params":{"app_id":"2220391788200892","exp_id":"null","is_from_share":false},"actor_id":"'+self.actor_id+'","client_mutation_id":"1"},"inviteShortLinkKey":null,"isChainingRecommendationUnit":false,"isEntityMenu":true,"scale":2,"source":"GROUP_MALL","renderLocation":"group_mall","__relay_internal__pv__GroupsCometEntityMenuEmbeddedrelayprovider":true,"__relay_internal__pv__GlobalPanelEnabledrelayprovider":false}',
            'server_timestamps': 'true',
            'doc_id': '5853134681430324',
            'fb_api_analytics_tags': '["qpl_active_flow_ids=431626709"]',
        }
        try:
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies, timeout=15)
            if self.actor_id in response.text:
                return True
            else:
                return False
        except Exception as e:
            return {'error': f'Proxy/Network error: {str(e)}'}
    def follow(self, id):
        data = {
            'av': self.actor_id,
            '__aaid': '0',
            '__user': self.actor_id,
            '__a': '1',
            '__req': '1i',
            '__hs': '20404.HYP:comet_pkg.2.1...0',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1029768321',
            '__s': 'pltptf:ea67kn:unlyfw',
            '__hsi': '7571827220565665323',
            '__dyn': '7xeUjGU9k9wxxt0koC8G6Ejh941twWwIxu13wFG3OubyQdwSAx-bwNwnof8boG4E762S1DwUx60xU8E5O0BU2_CxS320qa2OU7m2210wEwgo9oO0wE7u12wOx62G5Usw9m1cwLwBgK7o8o4u1uwoE4G17yovwRwlE-U2exi4UaEW4UWu1jxS6Fobrwh8lwUwOzEjUlDw-wUwxwhFVovUaU3VwLyEbUGdG0HE88cA0z8c84p1e4UK2K2WEjxK2B08-Utyo566k1fxC13xecwBwWzUfHDzUiBG2OUqwjVqwLwHwa211wo83KwHwOyUqxG0HE',
            '__csr': 'gdIA5RghYfORkhf3chOOlkn59iY9NV7d5N74icykjNtj8DiKzAIATOe-Jt4F-xx5tHWmhGvmmVppXrmVdEJqLGBhfALq9FuigzXQqYzGhfASjQ8mpbJeAFaHGGQit9delblqD_Z5h4AuGIBeQrh4BAjK9QGRGEy-8GfK4aQhatyGyXCAAKETh99aBy_iGuy9bGECFiASuKl5viBACCuFby5zkmt4VdppUgzEOLypHDKijzUZd4AnyqBKQbF4zay9qCQazrABG9Q6EVt1jBAyu8iylDVEOiAmQdm8hEWi59ogJ28-uAfGU--4aCGEGmmqbyrDxeGUmQby98Gu48mKV-umucCKqirBV8KbhUrhqKmq2J4QdUWeyoZ12FEDxu2B1CrhqxG6oryUO2DCgSu68izrxO8DF1Cu2i5oC1kwQAhofoO8Azolypaz8-awMxO7ayUb_xS6o5-dGu224USqp5DyVU9EnzobUhUkx22a1GwUxy0FFogwuEGE-1Uxa11xa9xO36486mUyubyUaEzU4W18yHACUqK2-5Ekx2fgOU99EW2y49U9EDgoxd1BF6xW11z8iABCBV9ogG1dU466UkwhElwlEnxqawXAwNBGt0m819KjU5508a042RXysa0Lwba0Su04dU3fg5O580g5zm3y0oC3WJ01GB1t0GgP80Zo1mE0Vmaz8-0cUyoC1Awr8S0gq2O9p9FS05oqw11u0Mxaxq6E0kwg08pE0bA8x24088w1RGU0u3w6Mw8a13g1TocbAfl2o9FA0oa0PS683txa0M9io5d0nofQ0kqUbu09Oo1bYg1DKq1owlEhw3H82Oo1so15V8G3UMW3q2hwroqweW0oS-0KQ7nwpFo3fwo81dVQ1Jx9w2Yo5e2ExE0wC1hwhUiw4mgrx20Wt0zjCl4z9C6V4Zw2hoaU3kFzoUjAfHTIOwiEig62cyNt6zpVFo8k7821wr8poaU0gLw1kd09C0RXw3mi073jg14Uixp28B38do6i08Sw2Y103ZzC1emlyoO0pa1Hw3A8cU4m6qxK2i17xt0b-3YM1GC0nu9gO2W0tq0B98fi5V-EgUpw3j411xpDykcEU2Mg3klwai1tw9m0qG09qxK',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            '__spin_r': '1014584891',
            '__spin_b': 'trunk',
            '__spin_t': '1719764873',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUserFollowMutation',
            'variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1719765181042,489343,250100865708545,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,unexpected,1719765155735,648442,391724414624676,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,tap_search_bar,1719765153341,865155,391724414624676,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"'+str(id)+'","tracking":null,"actor_id":"'+str(self.actor_id)+'","client_mutation_id":"5"},"scale":1}',
            'server_timestamps': 'true',
            'doc_id': '25581663504782089',
        }
        try:
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies, timeout=15)
            if '<!DOCTYPE html>' in response.text or '<html' in response.text:
                return {'error': 'HTML_ERROR', 'response': response.text}
            if '"subscribe_status":"IS_SUBSCRIBED"' in response.text:
                return True
            else:
                return {'error': 'Failed', 'response': response.text}
        except Exception as e:
            return {'error': f'Proxy/Network error: {str(e)}'}
    def getPages(self):
        try:
            payload = {
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'lsd': self.lsd,
                'fb_api_req_friendly_name': 'CometProfileSwitcherDialogQuery',
                'variables': '{"scale":2}',
                'doc_id': '5300338636681652'
            }
            response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=payload, proxies=self.proxies, timeout=15)
            data = response.json()
            pages = []
            viewer_data = data.get('data', {}).get('viewer', {})
            actor_data = viewer_data.get('actor', {})
            admined_nodes = viewer_data.get('admined_pages', {}).get('nodes', [])
            if not admined_nodes:
                admined_nodes = viewer_data.get('adminedPages', {}).get('nodes', [])
            for node in admined_nodes:
                page_id = node.get('id')
                page_name = node.get('name')
                if page_id and page_name:
                    pages.append({'id': page_id, 'name': page_name})
            if not pages:
                switcher_nodes = actor_data.get('profile_switcher_eligible_profiles', {}).get('nodes', [])
                for node in switcher_nodes:
                    profile = node.get('profile', {})
                    page_id = profile.get('id')
                    page_name = profile.get('name')
                    delegate_page_id = profile.get('delegate_page_id')  # LẤY delegate_page_id
                    if page_id and page_name and page_id != actor_data.get('id'):
                        pages.append({
                            'id': page_id,
                            'name': page_name,
                            'delegate_page_id': delegate_page_id  # Lưu delegate_page_id để lấy token
                        })
            if not pages:
                delegate_page_id = actor_data.get('delegate_page_id')
                if delegate_page_id:
                    pages.append({
                        'id': delegate_page_id,
                        'name': f'Page {delegate_page_id}',
                        'delegate_page_id': delegate_page_id
                    })
            return pages
        except Exception as e:
            return []
    def getPageToken(self, access_token):
        try:
            url = f'https://graph.facebook.com/me/accounts?access_token={access_token}'
            response = requests.get(url, proxies=self.proxies, timeout=15)
            data = response.json()
            page_tokens = {}
            for page in data.get('data', []):
                page_id = page.get('id')
                page_token = page.get('access_token')
                page_name = page.get('name')
                if page_id and page_token:
                    page_tokens[page_id] = {
                        'token': page_token,
                        'name': page_name
                    }
            return page_tokens
        except Exception as e:
            return {}    
    def getPages(self, user_token=None):
        try:
            payload = {
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'lsd': self.lsd,
                'fb_api_req_friendly_name': 'CometProfileSwitcherDialogQuery',
                'variables': '{"scale":2}',
                'doc_id': '5300338636681652'
            }

            response = requests.post(
                'https://www.facebook.com/api/graphql/',
                headers=self.headers,
                data=payload,
                proxies=self.proxies,
                timeout=15
            )

            data = response.json()

            pages = []
            viewer_data = data.get('data', {}).get('viewer', {})
            actor_data = viewer_data.get('actor', {})

            admined_nodes = viewer_data.get('admined_pages', {}).get('nodes', [])
            if not admined_nodes:
                admined_nodes = viewer_data.get('adminedPages', {}).get('nodes', [])

            # ===== lấy page từ graphql =====
            for node in admined_nodes:
                page_id = node.get('id')
                page_name = node.get('name')

                if page_id and page_name:
                    pages.append({
                        "id": page_id,
                        "name": page_name
                    })

            # fallback
            if not pages:
                switcher_nodes = actor_data.get('profile_switcher_eligible_profiles', {}).get('nodes', [])
                for node in switcher_nodes:
                    profile = node.get('profile', {})
                    page_id = profile.get('id')
                    page_name = profile.get('name')

                    if page_id and page_name and page_id != actor_data.get('id'):
                        pages.append({
                            "id": page_id,
                            "name": page_name
                        })

            # ====== MERGE PAGE TOKEN FROM USER TOKEN ======
            if user_token:
                token_map = self.getPageTokensFromUserToken(user_token)

                for p in pages:
                    page_id = p.get("id")
                    if page_id in token_map:
                        p["access_token"] = token_map[page_id]["access_token"]

            return pages

        except:
            return []
    def getPageTokensFromUserToken(self, user_token):
        try:
            url = "https://graph.facebook.com/v19.0/me/accounts"
            params = {
                "access_token": user_token
            }

            r = requests.get(url, params=params, timeout=15)
            data = r.json()

            pages = {}

            for p in data.get("data", []):
                pages[p["id"]] = {
                    "name": p.get("name"),
                    "access_token": p.get("access_token")
                }

            return pages

        except:
            return {}  
    def getPageTokensOnly(self, user_token):
        try:
            url = "https://graph.facebook.com/v19.0/me/accounts"
            params = {
                "access_token": user_token
            }

            r = requests.get(url, params=params, timeout=15)
            data = r.json()

            tokens = []

            for p in data.get("data", []):
                token = p.get("access_token")
                if token:
                    tokens.append(token)

            return tokens

        except:
            return []  
    def get_cookie_info(self):
        try:
            info = self.checkCookie()

            if "success" not in info:
                return None

            return {
                "uid": info["id"],
                "name": info["name"],
                "user_token": self.getAccessToken()
            }

        except:
            return None  
import random
import string
import json
import time
import requests
import uuid
import pyotp
import base64
import io
import struct
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


class FacebookPasswordEncryptor:
    @staticmethod
    def get_public_key():
        try:
            url = 'https://b-graph.facebook.com/pwd_key_fetch'
            params = {
                'version': '2',
                'flow': 'CONTROLLER_INITIALIZATION',
                'method': 'GET',
                'fb_api_req_friendly_name': 'pwdKeyFetch',
                'fb_api_caller_class': 'com.facebook.auth.login.AuthOperations',
                'access_token': '438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28'
            }
            response = requests.post(url, params=params).json()
            return response.get('public_key'), str(response.get('key_id', '25'))
        except Exception as e:
            raise Exception(f"Không thể lấy public key: {e}")

    @staticmethod
    def encrypt(password, public_key=None, key_id="25"):
        if public_key is None:
            public_key, key_id = FacebookPasswordEncryptor.get_public_key()

        try:
            rand_key = get_random_bytes(32)
            iv = get_random_bytes(12)
            
            pubkey = RSA.import_key(public_key)
            cipher_rsa = PKCS1_v1_5.new(pubkey)
            encrypted_rand_key = cipher_rsa.encrypt(rand_key)
            
            cipher_aes = AES.new(rand_key, AES.MODE_GCM, nonce=iv)
            current_time = int(time.time())
            cipher_aes.update(str(current_time).encode("utf-8"))
            encrypted_passwd, auth_tag = cipher_aes.encrypt_and_digest(password.encode("utf-8"))
            
            buf = io.BytesIO()
            buf.write(bytes([1, int(key_id)]))
            buf.write(iv)
            buf.write(struct.pack("<h", len(encrypted_rand_key)))
            buf.write(encrypted_rand_key)
            buf.write(auth_tag)
            buf.write(encrypted_passwd)
            
            encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"#PWD_FB4A:2:{current_time}:{encoded}"
        except Exception as e:
            raise Exception(f"Lỗi khi mã hóa mật khẩu: {e}")


class FacebookAppTokens:
    APPS = {
        'FB_ANDROID': {'name': 'Facebook For Android', 'app_id': '350685531728'},
        'MESSENGER_ANDROID': {'name': 'Facebook Messenger For Android', 'app_id': '256002347743983'},
        'FB_LITE': {'name': 'Facebook For Lite', 'app_id': '275254692598279'},
        'MESSENGER_LITE': {'name': 'Facebook Messenger For Lite', 'app_id': '200424423651082'},
        'ADS_MANAGER_ANDROID': {'name': 'Ads Manager App For Android', 'app_id': '438142079694454'},
        'PAGES_MANAGER_ANDROID': {'name': 'Pages Manager For Android', 'app_id': '121876164619130'}
    }
    
    @staticmethod
    def get_app_id(app_key):
        app = FacebookAppTokens.APPS.get(app_key)
        return app['app_id'] if app else None
    
    @staticmethod
    def get_all_app_keys():
        return list(FacebookAppTokens.APPS.keys())
    
    @staticmethod
    def extract_token_prefix(token):
        for i, char in enumerate(token):
            if char.islower():
                return token[:i]
        return token


class FacebookLogin:
    API_URL = "https://b-graph.facebook.com/auth/login"
    ACCESS_TOKEN = "350685531728|62f8ce9f74b12f84c123cc23437a4a32"
    API_KEY = "882a8490361da98702bf97a021ddc14d"
    SIG = "214049b9f17c38bd767de53752b53946"
    
    BASE_HEADERS = {
        "content-type": "application/x-www-form-urlencoded",
        "x-fb-net-hni": "45201",
        "zero-rated": "0",
        "x-fb-sim-hni": "45201",
        "x-fb-connection-quality": "EXCELLENT",
        "x-fb-friendly-name": "authenticate",
        "x-fb-connection-bandwidth": "78032897",
        "x-tigon-is-retry": "False",
        "authorization": "OAuth null",
        "x-fb-connection-type": "WIFI",
        "x-fb-device-group": "3342",
        "priority": "u=3,i",
        "x-fb-http-engine": "Liger",
        "x-fb-client-ip": "True",
        "x-fb-server-cluster": "True"
    }
    
    def __init__(self, uid_phone_mail, password, twwwoo2fa="", machine_id=None, convert_token_to=None, convert_all_tokens=False):
        self.uid_phone_mail = uid_phone_mail
        self.twwwoo2fa = twwwoo2fa
        
        if password.startswith("#PWD_FB4A"):
            self.password = password
        else:
            self.password = FacebookPasswordEncryptor.encrypt(password)
        
        if convert_all_tokens:
            self.convert_token_to = FacebookAppTokens.get_all_app_keys()
        elif convert_token_to:
            self.convert_token_to = convert_token_to if isinstance(convert_token_to, list) else [convert_token_to]
        else:
            self.convert_token_to = []
        
        self.session = requests.Session()
        
        self.device_id = str(uuid.uuid4())
        self.adid = str(uuid.uuid4())
        self.secure_family_device_id = str(uuid.uuid4())
        self.machine_id = machine_id if machine_id else self._generate_machine_id()
        self.jazoest = ''.join(random.choices(string.digits, k=5))
        self.sim_serial = ''.join(random.choices(string.digits, k=20))
        
        self.headers = self._build_headers()
        self.data = self._build_data()
    
    @staticmethod
    def _generate_machine_id():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    
    def _build_headers(self):
        headers = self.BASE_HEADERS.copy()
        headers.update({
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}',
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23113RKC6C Build/PQ3A.190705.08211809) [FBAN/FB4A;FBAV/417.0.0.33.65;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/480086274;FBCR/MobiFone;FBMF/Redmi;FBBD/Redmi;FBDV/23113RKC6C;FBSV/9;FBCA/x86:armeabi-v7a;FBDM/{density=1.5,width=1280,height=720};FB_FW/1;FBRV/0;]"
        })
        return headers
    
    def _build_data(self):
        base_data = {
            "format": "json",
            "email": self.uid_phone_mail,
            "password": self.password,
            "credentials_type": "password",
            "generate_session_cookies": "1",
            "locale": "vi_VN",
            "client_country_code": "VN",
            "api_key": self.API_KEY,
            "access_token": self.ACCESS_TOKEN
        }
        
        base_data.update({
            "adid": self.adid,
            "device_id": self.device_id,
            "generate_analytics_claim": "1",
            "community_id": "",
            "linked_guest_account_userid": "",
            "cpl": "true",
            "try_num": "1",
            "family_device_id": self.device_id,
            "secure_family_device_id": self.secure_family_device_id,
            "sim_serials": f'["{self.sim_serial}"]',
            "openid_flow": "android_login",
            "openid_provider": "google",
            "openid_tokens": "[]",
            "account_switcher_uids": f'["{self.uid_phone_mail}"]',
            "fb4a_shared_phone_cpl_experiment": "fb4a_shared_phone_nonce_cpl_at_risk_v3",
            "fb4a_shared_phone_cpl_group": "enable_v3_at_risk",
            "enroll_misauth": "false",
            "error_detail_type": "button_with_disabled",
            "source": "login",
            "machine_id": self.machine_id,
            "jazoest": self.jazoest,
            "meta_inf_fbmeta": "V2_UNTAGGED",
            "advertiser_id": self.adid,
            "encrypted_msisdn": "",
            "currently_logged_in_userid": "0",
            "fb_api_req_friendly_name": "authenticate",
            "fb_api_caller_class": "Fb4aAuthHandler",
            "sig": self.SIG
        })
        
        return base_data
    
    def _convert_token(self, access_token, target_app):
        try:
            app_id = FacebookAppTokens.get_app_id(target_app)
            if not app_id:
                return None
            
            response = requests.post(
                'https://api.facebook.com/method/auth.getSessionforApp',
                data={
                    'access_token': access_token,
                    'format': 'json',
                    'new_app_id': app_id,
                    'generate_session_cookies': '1'
                }
            )
            
            result = response.json()
            
            if 'access_token' in result:
                token = result['access_token']
                prefix = FacebookAppTokens.extract_token_prefix(token)
                
                cookies_dict = {}
                cookies_string = ""
                
                if 'session_cookies' in result:
                    for cookie in result['session_cookies']:
                        cookies_dict[cookie['name']] = cookie['value']
                        cookies_string += f"{cookie['name']}={cookie['value']}; "
                
                return {
                    'token_prefix': prefix,
                    'access_token': token,
                    'cookies': {
                        'dict': cookies_dict,
                        'string': cookies_string.rstrip('; ')
                    }
                }
            
            return None
                
        except:
            return None
    
    def _parse_success_response(self, response_json):
        original_token = response_json.get('access_token')
        original_prefix = FacebookAppTokens.extract_token_prefix(original_token)
        
        result = {
            'success': True,
            'original_token': {
                'token_prefix': original_prefix,
                'access_token': original_token
            },
            'cookies': {}
        }
        
        if 'session_cookies' in response_json:
            cookies_dict = {}
            cookies_string = ""
            for cookie in response_json['session_cookies']:
                cookies_dict[cookie['name']] = cookie['value']
                cookies_string += f"{cookie['name']}={cookie['value']}; "
            result['cookies'] = {
                'dict': cookies_dict,
                'string': cookies_string.rstrip('; ')
            }
        
        if self.convert_token_to:
            result['converted_tokens'] = {}
            for target_app in self.convert_token_to:
                converted = self._convert_token(original_token, target_app)
                if converted:
                    result['converted_tokens'][target_app] = converted
        
        return result
    
    def _handle_2fa(self, error_data):
        if not self.twwwoo2fa:
            return {'success': False, 'error': 'Cần mã 2FA nhưng chưa được cung cấp'}
        
        try:
            twofactor_code = pyotp.TOTP(self.twwwoo2fa).now()
            
            data_2fa = {
                'locale': 'vi_VN',
                'format': 'json',
                'email': self.uid_phone_mail,
                'device_id': self.device_id,
                'access_token': self.ACCESS_TOKEN,
                'generate_session_cookies': 'true',
                'generate_machine_id': '1',
                'twofactor_code': twofactor_code,
                'credentials_type': 'two_factor',
                'error_detail_type': 'button_with_disabled',
                'first_factor': error_data['login_first_factor'],
                'password': self.password,
                'userid': error_data['uid'],
                'machine_id': error_data['login_first_factor']
            }
            
            response = self.session.post(self.API_URL, data=data_2fa, headers=self.headers)
            response_json = response.json()
            
            if 'access_token' in response_json:
                return self._parse_success_response(response_json)
            elif 'error' in response_json:
                return {
                    'success': False,
                    'error': response_json['error'].get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {'success': False, 'error': f'Lỗi 2FA: {str(e)}'}
    
    def login(self):
        try:
            response = self.session.post(self.API_URL, headers=self.headers, data=self.data)
            response_json = response.json()
            
            if 'access_token' in response_json:
                return self._parse_success_response(response_json)
            
            if 'error' in response_json:
                error_data = response_json.get('error', {}).get('error_data', {})
                
                if 'login_first_factor' in error_data and 'uid' in error_data:
                    return self._handle_2fa(error_data)
                
                return {
                    'success': False,
                    'error': response_json['error'].get('message', 'Unknown error'),
                    'error_user_msg': response_json['error'].get('error_user_msg')
                }
            
            return {'success': False, 'error': 'Unknown response format'}
            
        except json.JSONDecodeError:
            return {'success': False, 'error': 'Response không phải JSON hợp lệ'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
if __name__ == "__main__":

    uid_phone_mail = "61569230780984"

    password = "Wuposoye@163391"

    twwwoo2fa = "".replace(" ", "")

    machine_id = "d9LQaYoTJdxE9GO12peAOO9U" #Nếu báo sai mật khẩu thì lấy giá trị của cookies acc đó gán vào datr=_2KxZzOokdiTAQGEsqoFdRJk;
    
    fb_login = FacebookLogin(
        uid_phone_mail=uid_phone_mail,
        password=password,
        twwwoo2fa=twwwoo2fa,
        machine_id=machine_id,
        convert_all_tokens=True
    )
    
    result = fb_login.login()
    
    if result['success']:
        print("=" * 80)
        print(f"{result['original_token']['token_prefix']}")
        print("=" * 80)
        print(f"{result['original_token']['access_token']}\n")
        
        if 'converted_tokens' in result and result['converted_tokens']:
            print("=" * 80)
            print("CONVERTED TOKENS")
            print("=" * 80)
            for app_key, token_data in result['converted_tokens'].items():
                print(f"\n{token_data['token_prefix']}:")
                print(f"{token_data['access_token']}")
        
        print("\n" + "=" * 80)
        print("COOKIES")
        print("=" * 80)
        print(result['cookies']['string'])
    else:
        print("=" * 80)
        print("LOGIN FAILED")
        print("=" * 80)
        print(f"Error: {result.get('error')}")                       
# ... toàn bộ code thật của mày
"""

import types

# ================= INIT MODULE =================
fb_module = types.ModuleType("FB_WEB_API")

# load code chính (API, session...)
exec(FB_WEB_API_CODE, fb_module.__dict__)



# ================= EXPOSE CLASS =================
FacebookSession = fb_module.FacebookSession
FB_API = fb_module.FB_API
HTMLExtractor = fb_module.HTMLExtractor
NumberEncoder = fb_module.NumberEncoder
CookieHandler = fb_module.CookieHandler
GenData = fb_module.GenData
facebookDapi = fb_module.facebookDapi
GolikeAPI = fb_module.GolikeAPI

# thêm cái bạn vừa inject
FacebookLogin = fb_module.FacebookLogin
FacebookPasswordEncryptor = fb_module.FacebookPasswordEncryptor
FacebookAppTokens = fb_module.FacebookAppTokens

class AppCLI:
    def __init__(self):
        self.fb_accounts = []
        self.gl_accounts = []
        self.golike_token = ""
        self.running = False
        self.job_config = {"max_jobs": 999,"types": ["all"]}
        self.selected = []
        self.table = {}
        self.run_mode = "cookie"
        self.pfbid_cache = {}
        self.load_data()

      

    # ================= MENU =================
    def menu(self):
        while True:
            print("\n===== MENU =====")
            print("1. Nhập cookie")
            print("2. Check cookie")
            print("3. Login Golike")
            print("4. Chọn acc")
            print("5. Bắt đầu chạy JOB")
            print("6. Xóa acc")
            print("7. Login UID + PASS + COOKIE")
            print("8. Nhập acc từ file accounts_fb.txt")
            print("0. Thoát")

            c = input(">>Chọn: ")

            if c == "1":
                self.input_cookie()
            elif c == "2":
                self.check_cookies()
            elif c == "3":
                self.login_golike()
            elif c == "4":
                self.select_accounts()
            elif c == "5":
                self.start_job()
            elif c == "6":
                self.delete_account()
            elif c == "7":
                self.login_simple()  
            elif c == "8":
                self.load_accounts_from_file()
            elif c == "0":
                self.save_data()
                break

    # ================= INPUT =================
    def input_cookie(self):
        print("Nhập: cookie|token|ip:port:user:pass (Enter trống để chạy check)")
        i = 1

        new_indexes = []

        while True:
            line = input(f"[{i}] > ").strip()
            if not line:
                break

            parts = line.split("|")

            if len(parts) < 2:
                print("❌ Format: cookie|token|proxy")
                continue

            cookie = parts[0].strip()
            token = parts[1].strip()

            proxy = None
            if len(parts) >= 3:
                proxy = self.format_proxy(parts[2].strip())

            self.fb_accounts.append({
                "cookie": cookie,
                "token": token,
                "proxy": proxy,   # 🔥 FIX
                "new": True
            })

            new_indexes.append(len(self.fb_accounts) - 1)
            i += 1

        if new_indexes:
            print(f"\n🚀 Bắt đầu check {len(new_indexes)} acc...\n")
            self.check_cookies(auto_select=new_indexes)
    def format_proxy(self, proxy):
        if not proxy:
            return None

        try:
            parts = proxy.split(":")

            # ip:port:user:pass
            if len(parts) == 4:
                ip, port, user, password = parts
                proxy_url = f"http://{user}:{password}@{ip}:{port}"

            # ip:port
            elif len(parts) == 2:
                ip, port = parts
                proxy_url = f"http://{ip}:{port}"

            else:
                return None

            return {
                "http": proxy_url,
                "https": proxy_url
            }

        except:
            print("❌ Proxy lỗi định dạng!")
            return None
    # ================= CHECK =================
    def check_cookies(self, auto_select=None,):
        new_list = []
        # =========================
        # HIỂN THỊ DANH SÁCH
        # =========================
        print("\n===== DANH SÁCH ACC =====")
        for i, acc in enumerate(self.fb_accounts, 1):
            name = acc.get("name", "Unknown")
            uid = acc.get("uid", "???")
            print(f"{i}. {name} | {uid}")

        # =========================
        # CHỌN ACC
        # =========================
        if auto_select is not None:
            selected_index = auto_select
            print(f"🔄 Auto check acc mới: {[i+1 for i in selected_index]}")
        else:
            choose = input("Nhập số acc muốn check (vd: 1 3 5): ").strip()

            if not choose:
                print(" Không chọn gì")
                return

            try:
                selected_index = [int(x) - 1 for x in choose.split()]
            except:
                print(" Sai định dạng")
                return

        # =========================
        # LOOP
        # =========================
        for i, acc in enumerate(self.fb_accounts):

            # 🔥 nếu không nằm trong danh sách chọn → giữ nguyên
            if i not in selected_index:
                new_list.append(acc)
                continue

            cookie = acc.get("cookie")
            user_token = acc.get("token")
            proxies = acc.get("proxy") 
            try:
                fb = facebookDapi(cookie)
                info = fb.checkCookie()

                if "success" in info:
                    uid = info["id"]
                    name = info["name"]

                    print(f" {name} | {uid}")

                    # =========================
                    # 1. LẤY PAGE TOKEN
                    # =========================
                    page_token_map = {}

                    try:
                        r = requests.get(
                            "https://graph.facebook.com/v19.0/me/accounts",
                            params={"access_token": user_token},
                            proxies=proxies,
                            timeout=15
                        )

                        for p in r.json().get("data", []):
                            pname = p.get("name")
                            ptoken = p.get("access_token")

                            if pname and ptoken:
                                page_token_map[pname] = ptoken

                    except Exception as e:
                        print("❌ Lỗi lấy page token:", e)

                    # =========================
                    # 2. LẤY PAGE LIST
                    # =========================
                    pages = []

                    for p in fb.getPages():
                        pid = p["id"]
                        pname = p["name"]

                        page_cookie = cookie + f";i_user={pid};"

                        pages.append({
                            "id": pid,
                            "name": pname,
                            "cookie": page_cookie,
                            "token": page_token_map.get(pname)
                        })

                    # =========================
                    # UPDATE ACC
                    # =========================
                    new_list.append({
                        "uid": uid,
                        "name": name,
                        "cookie": cookie,
                        "token": user_token,
                        "pages": pages,
                        "proxy": proxies
                    })

                else:
                    print(f"❌ DIE acc index {i+1}")
                    new_list.append(acc)

            except Exception as e:
                print("❌", e)
                new_list.append(acc)

        self.fb_accounts = new_list

        # =========================
        # 🔥 CLEAN DATA
        # =========================

        # ❌ Xóa acc lỗi (không có uid/name)
        self.fb_accounts = [
            acc for acc in self.fb_accounts
            if acc.get("uid") and acc.get("name")
        ]

        # ❌ Xóa acc trùng cookie
        seen = set()
        clean = []

        for acc in self.fb_accounts:
            cookie = acc.get("cookie")
            if cookie not in seen:
                seen.add(cookie)
                clean.append(acc)

        self.fb_accounts = clean

        # =========================
        self.save_data()
    # ================= LOGIN =================
    def login_golike(self):
        if self.golike_token:
            token = self.golike_token
            print(" Đang dùng token đã lưu...")
        else:
            token = input("Nhập Token Golike: ")
            self.golike_token = token

        api = GolikeAPI(token)
        user = api.get_user_info()

        if not user:
            print(" Token lỗi, vui lòng nhập lại")
            self.golike_token = ""
            return

        print(f" {user['name']} | Xu: {user['coin']}")
        self.gl_accounts = api.get_fb_info() or []
        self.save_data()

    # ================= SELECT =================
    def select_accounts(self):
        self.selected = []
        mapping = {}
        idx = 1

        print("\n===== DANH SÁCH ACC/PAGE (GROUP) =====\n")

        for acc in self.fb_accounts:
            print(f"👤 [{idx}] USER: {acc['name']} | {acc['uid']}")
            mapping[idx] = ("user", acc)
            idx += 1

            # 👉 BOX PAGE
            if acc.get("pages"):
                print("   ├── 📄 PAGES:")
                for p in acc.get("pages", []):
                    print(f"   │    [{idx}] {p['name']} | {p['id']}")
                    mapping[idx] = ("page", acc, p)
                    idx += 1

            print("   └────────────────────────")

        print("\nChọn (vd: 1,2,5 | all | all_acc | all_page): ")
        picks = input(">> ").strip().lower()

        # ===== CHỌN TẤT CẢ =====
        if picks == "all":
            self.selected = list(mapping.values())

        elif picks == "all_acc":
            self.selected = [v for v in mapping.values() if v[0] == "user"]

        elif picks == "all_page":
            self.selected = [v for v in mapping.values() if v[0] == "page"]

        else:
            for p in picks.split(","):
                try:
                    self.selected.append(mapping[int(p.strip())])
                except:
                    pass

        print(f"\n✅ Đã chọn {len(self.selected)} acc/page\n")

    # ================= TABLE =================
    def build_table(self):
        panels = []
        for uid, d in self.table.items():
            # ===== STATUS WRAP =====
            status_text = Text(d["status"], overflow="fold")
            status_text.no_wrap = False

            content = Text(no_wrap=False, overflow="fold")

            # ===== 🔥 FIX PROXY =====
            proxy = d.get("proxy")

            if isinstance(proxy, dict):
                proxy = proxy.get("http", "")

            # 👉 bỏ http:// cho gọn
            if isinstance(proxy, str):
                proxy = proxy.replace("http://", "").replace("https://", "")

                # 👉 nếu có user:pass@host → lấy host thôi (optional)
                # proxy = proxy.split("@")[-1]

            if not proxy:
                proxy = "Không dùng"

            # ===== CONTENT =====
            content.append(f"UID: {uid}\n", style="bold")
            content.append(f"Tên FaceBook: {d['name']}\n", style="bold")
            content.append(f"Tiền Kiếm được: {d['xu']}\n", style="bold")
            content.append(f"Thành công: {d['success']}\n", style="bold")
            content.append(f"Lỗi: {d['fail']}\n", style="bold")

            # 👉 proxy màu khác cho dễ nhìn
            content.append("Proxy: ", style="bold")
            content.append(f"{proxy}\n", style="cyan")

            content.append(f"Chế độ: {self.run_mode}\n", style="bold")
            content.append("Hành Động:\n", style="bold")
            content.append(status_text)

            # ===== COLOR PANEL =====
            status_upper = d["status"].upper()

            if "ERROR" in status_upper or "FAIL" in status_upper:
                color = "red"
            elif "THÀNH CÔNG" in status_upper or "+" in status_upper:
                color = "green"
            else:
                color = "yellow"

            panel = Panel(
                content,
                title=f"ACC {d['name']}",
                border_style=color,
                width=50,
                height=12
            )

            panels.append(panel)

        return Columns(panels, expand=True)

    # ================= START =================
    def start_job(self):
        if not self.selected:
            print(" chưa chọn acc")
            return

        if not self.golike_token:
            print(" chưa login golike")
            return

        self.choose_job_config()
        self.choose_mode()
        self.running = True

        api = GolikeAPI(self.golike_token)
        self.gl_accounts = api.get_fb_info() or []
        gl_ids = set(str(acc["fb_id"]) for acc in self.gl_accounts)

        self.table = {}  # 🔥 reset bảng

        # ================= INIT TABLE =================
        for item in self.selected:
            if item[0] == "user":
                acc = item[1]
                fb_acc = {
                    "uid": acc["uid"],
                    "name": acc["name"],
                    "cookie": acc["cookie"],
                    "token": acc.get("token"),
                    "proxy": acc.get("proxy")
                }
            else:
                acc = item[1]
                p = item[2]
                page_cookie = acc["cookie"] + f";i_user={p['id']};"

                fb_acc = {
                    "uid": p["id"],
                    "name": p["name"],
                    "cookie": page_cookie,
                    "token": p.get("token"),
                    "proxy": acc.get("proxy")
                }

            fb_id = str(fb_acc["uid"])

            # 🔥 DEBUG nếu cần
            # print("INIT:", fb_acc)

            self.table[fb_id] = {
                "name": fb_acc["name"],
                "xu": 0,
                "success": 0,
                "fail": 0,
                "status": "Khởi động",
                "proxy": fb_acc.get("proxy")  # 🔥 QUAN TRỌNG
            }

        # ================= CLEAR =================
        os.system("cls" if os.name == "nt" else "clear")

        # ================= LIVE TABLE =================
        with Live(self.build_table(), refresh_per_second=2, screen=True) as live:

            # ================= START THREAD =================
            for item in self.selected:
                if item[0] == "user":
                    acc = item[1]
                    fb_acc = {
                        "uid": acc["uid"],
                        "name": acc["name"],
                        "cookie": acc["cookie"],
                        "token": acc.get("token"),
                        "proxy": acc.get("proxy")
                    }
                else:
                    acc = item[1]
                    p = item[2]
                    page_cookie = acc["cookie"] + f";i_user={p['id']};"

                    fb_acc = {
                        "uid": p["id"],
                        "name": p["name"],
                        "cookie": page_cookie,
                        "token": p.get("token"),
                        "proxy": acc.get("proxy")
                    }

                fb_id = str(fb_acc["uid"])

                def worker(fb_acc=fb_acc, fb_id=fb_id):
                    try:
                        # ===== CHECK GOLIKE =====
                        self.table[fb_id]["status"] = "Check Golike..."

                        if fb_id not in gl_ids:
                            self.table[fb_id]["status"] = "VERIFY..."

                            result = self.auto_verify_golike(fb_acc)
                            msg = result["message"].lower()

                            if not result["success"]:
                                self.table[fb_id]["status"] = msg
                                return

                            if "chờ" in msg or "duyệt" in msg:
                                self.table[fb_id]["status"] = msg
                                return

                            self.table[fb_id]["status"] = "VERIFY OK"

                            # ===== WAIT 120s =====
                            for i in range(120, 0, -1):
                                bar = "█" * (120 - i) + "░" * i
                                self.table[fb_id]["status"] = f"Verify thành công | chờ {i}s\n{bar}"
                                time.sleep(1)

                        # ===== RUN JOB =====
                        if not self.gl_accounts:
                            self.table[fb_id]["status"] = "Không có Golike account"
                            return

                        gl = random.choice(self.gl_accounts)

                        self.run_jobs(fb_acc, gl["id"])

                    except Exception as e:
                        self.table[fb_id]["status"] = f"Lỗi: {str(e)[:50]}"

                threading.Thread(target=worker, daemon=True).start()

            # ================= LOOP UPDATE =================
            while self.running:
                live.update(self.build_table())
                time.sleep(0.1)
    def stop_job(self):
        self.running = False
        print(" Stopped")

    # ================= CORE =================
    def run_jobs(self, fb_acc, account_id):
        api = GolikeAPI(self.golike_token)
        fb_id = str(fb_acc["uid"])
        cookie = fb_acc["cookie"]
        proxy = fb_acc.get("proxy")
        proxies = proxy if proxy else None
        xu_total = 0
        success_count = 0
        fail_count = 0
        done_count = 0  # 🔥 đếm job

        fb = FB_API(cookie)
        job_repeat = {}
        current_sv = "sv?"

        # =========================
        # CONFIG
        # =========================
        job_config = getattr(self, "job_config", {"max_jobs": 999,"types": ["all"]})

        DONE_FILE = "done_jobs.json"

        # =========================
        # LOAD FILE
        # =========================
        if os.path.exists(DONE_FILE):
            try:
                with open(DONE_FILE, "r") as f:
                    all_done = json.load(f)
            except:
                all_done = {}
        else:
            all_done = {}

        if fb_id not in all_done:
            all_done[fb_id] = {"object_ids": {}, "job_ids": {}}

        done_objects = all_done[fb_id].get("object_ids", {})
        done_jobs = all_done[fb_id].get("job_ids", {})

        def clean_old():
            now = time.time()
            expire = 7 * 24 * 60 * 60

            for k in list(done_objects.keys()):
                if now - done_objects[k] > expire:
                    del done_objects[k]

            for k in list(done_jobs.keys()):
                if now - done_jobs[k] > expire:
                    del done_jobs[k]

        def save_done():
            all_done[fb_id]["object_ids"] = done_objects
            all_done[fb_id]["job_ids"] = done_jobs

            with open(DONE_FILE, "w") as f:
                json.dump(all_done, f, ensure_ascii=False, indent=2)
                

        # =========================
        # LOOP
        # =========================
        while self.running:

            # 🔥 LIMIT JOB
            if done_count >= job_config["max_jobs"]:
                self.table[fb_id]["status"] = f"Đã đạt {done_count} job → STOP"
                break

            clean_old()

            total_wait = random.randint(8, 12)

            for i in range(total_wait, 0, -1):
                if not self.running:
                    break

                bar = "█" * (total_wait - i) + "░" * i
                self.table[fb_id]["status"] = f"[{current_sv}] | Chờ job | {i}s | {bar}"
                time.sleep(1)

            self.table[fb_id]["status"] = f"[{current_sv}] | Đang lấy job..."

            # =========================
            # GET JOB
            # =========================
            try:
                jobs, current_sv = api.get_jobs(fb_id)
            except:
                self.table[fb_id]["status"] = "JOB ERROR"
                time.sleep(3)
                continue

            if not jobs:
                self.table[fb_id]["status"] = f"[{current_sv}] Không có job"
                time.sleep(2)
                continue

            # =========================
            # LOOP JOB
            # =========================
            for job in jobs:
                if not self.running:
                    break

                job_id = job.get("id")
                job_type = job.get("type")
                object_id = str(job.get("object_id", ""))

               # 🔥 FIX PFBID (CHỈ TOKEN MỚI CẦN)
                if self.run_mode == "token" and "pfbid" in object_id:
                    full_link = f"https://www.facebook.com/{object_id}"

                    new_id = self.convert_pfbid(full_link)

                    if new_id:
                        object_id = new_id
                        job["object_id"] = new_id
                    else:
                        self.table[fb_id]["status"] = f"[{current_sv}] | Convert pfbid lỗi → REPORT"
                        api.report_job(job_id, fb_id)
                        continue

                coin = job.get("fix_coin_job")
                link = f"https://facebook.com/{object_id}"

                # =========================
                # FILTER TYPE
                # =========================
                allowed = job_config["types"]

                all_reactions = ["like", "love", "care", "haha", "wow", "sad", "angry"]

                # nếu chọn reaction → ăn hết cảm xúc
                if "reaction" in allowed and job_type in all_reactions:
                    pass
                elif "all" not in allowed and job_type not in allowed:
                    continue

                # =========================
                # CHECK JOB CŨ
                # =========================
                if object_id in done_objects or job_id in done_jobs:
                    self.table[fb_id]["status"] = f"[{current_sv}] | JOB CŨ → REPORT"
                    try:
                        api.report_job(job_id, fb_id)
                    except:
                        pass
                    time.sleep(1)
                    continue

                job_repeat[job_id] = job_repeat.get(job_id, 0) + 1
                if job_repeat[job_id] >= 2:
                    continue

                # =========================
                # LABEL
                # =========================
                reaction = job_type.upper()
                if job_type == "review":
                    reaction = "COMMENT"
                elif job_type == "follow":
                    reaction = "FOLLOW"

                try:
                    # =========================
                    # WAIT ACTION
                    # =========================
                    for i in range(3, 0, -1):
                        self.table[fb_id]["status"] = (
                            f"[{current_sv}] | Lấy thành công job {reaction} (+{coin} xu) sau {i}s | {job_id}\n{link}"
                        )
                        time.sleep(1)

                    self.table[fb_id]["status"] = (
                        f"[{current_sv}] | Đang {reaction} (+{coin} xu) | {job_id}\n{link}"
                    )

                    # =========================
                    # ACTION
                    # =========================
                    if self.run_mode == "token":
                        

                        if job_type not in ["like", "love", "care", "haha", "wow", "sad", "angry"]:
                            self.table[fb_id]["status"] = f"[{current_sv}] | TOKEN chỉ reaction → SKIP"
                            continue

                        try:
                            url = f"https://graph.facebook.com/v23.0/{object_id}/reactions"
                            data = {
                                "type": job_type.upper(),
                                "access_token": fb_acc.get("token")
                            }
                            r = requests.post(url, data=data, proxies=proxies).json()

                            res = {"success": "error" not in r}

                        except:
                            res = {"success": False}

                    else:
                        # ✅ COOKIE → FULL
                        if job_type == "review":
                            message = job.get("comment_run", {}).get("message", "")
                            res = fb.CMT(cmt=message, Id_post=object_id)

                        elif job_type == "follow":
                            res = fb.FOLLOW(object_id)

                        else:
                            real_reaction = job.get("type", "like").upper()
                            res = fb.REACTION(real_reaction, object_id)

                    if not res or not res.get("success"):
                        fail_count += 1
                        self.table[fb_id]["fail"] = fail_count
                        self.table[fb_id]["status"] = f"[{current_sv}] | [{reaction}] thất bại → REPORT"
                        api.report_job(job_id, fb_id)
                        continue

                    # =========================
                    # CHECK SYNC
                    # =========================
                    if job_type in ["review", "follow"]:
                        check = True
                    else:
                        check = False
                        for i in range(3):
                            self.table[fb_id]["status"] = f"[{current_sv}] | check FB sync ({i+1}/3)"
                            time.sleep(2)
                            check = fb.CHECK_REACTION(object_id)
                            if check:
                                break

                    if not check:
                        self.table[fb_id]["status"] = f"[{current_sv}] | SKIP (FB chưa sync)"
                        continue

                    self.table[fb_id]["status"] = f"[{current_sv}] | {reaction} Thành công"

                    # =========================
                    # WAIT XU
                    # =========================
                    wait_time = random.randint(10, 15)
                    for i in range(wait_time, 0, -1):
                        bar = "█" * (wait_time - i) + "░" * i
                        self.table[fb_id]["status"] = f"[{current_sv}] | Chờ xu {i}s | {bar}"
                        time.sleep(1)

                    # =========================
                    # COMPLETE
                    # =========================
                    self.table[fb_id]["status"] = f"[{current_sv}] | Đang nhận xu..."
                    time.sleep(2.5)

                    done = api.complete_job(
                        job_id=job_id,
                        job_type=job_type,
                        object_id=object_id,
                        uid=fb_id,
                        fb_account_id=account_id,
                        advertising_id=job_id
                    )

                    if not isinstance(done, dict):
                        fail_count += 1
                        self.table[fb_id]["fail"] = fail_count
                        self.table[fb_id]["status"] = f"[{current_sv}] | COMPLETE ERROR"
                        continue

                    success_api = done.get("success", False)
                    msg_raw = done.get("message") or str(done)
                    msg_lower = msg_raw.lower()

                    match = re.search(r"(?:số\s*xu|xu)\D*(\d+)", msg_lower)
                    earned = int(match.group(1)) if match else 0

                    # =========================
                    # SUCCESS
                    # =========================
                    if success_api and earned > 0:
                        xu_total += earned
                        success_count += 1
                        done_count += 1  # 🔥 tăng job

                        self.table[fb_id]["xu"] = xu_total
                        self.table[fb_id]["success"] = success_count

                        self.table[fb_id]["status"] = f"[{current_sv}] | {msg_raw}"

                        now = time.time()
                        done_objects[object_id] = now
                        done_jobs[job_id] = now
                        save_done()

                    elif "chờ" in msg_lower or "duyệt" in msg_lower:
                        self.table[fb_id]["status"] = f"[{current_sv}] | {msg_raw}"

                    else:
                        fail_count += 1
                        self.table[fb_id]["fail"] = fail_count
                        self.table[fb_id]["status"] = f"[{current_sv}] | FAIL | {msg_raw}"

                except Exception as e:
                    fail_count += 1
                    self.table[fb_id]["fail"] = fail_count
                    self.table[fb_id]["status"] = f"[{current_sv}] ERROR: {str(e)[:50]}"

                time.sleep(random.uniform(2, 4))
    # ================= DATA =================
    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump({
                "fb_accounts": self.fb_accounts,
                "golike_token": self.golike_token,
                "job_config": self.job_config   
            }   , f, ensure_ascii=False, indent=2)

    def load_data(self):
        if not os.path.exists("data.json"):
            return

        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.fb_accounts = data.get("fb_accounts", [])
        self.golike_token = data.get("golike_token", "")
        self.job_config = data.get("job_config", {"max_jobs": 999,"types": ["all"]})
    def delete_account(self):
        print("===== DANH SÁCH ACC =====")
        for i, acc in enumerate(self.fb_accounts, 1):
            print(f"{i}. {acc.get('name')} | {acc.get('uid')}")

        raw = input("Chọn acc muốn xóa (vd: 1,3,5): ")

        try:
            indexes = sorted(
                [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()],
                reverse=True
            )
        except:
            print("Input lỗi")
            return

        deleted = []

        for i in indexes:
            if 1 <= i <= len(self.fb_accounts):
                acc = self.fb_accounts.pop(i - 1)
                deleted.append(acc.get("uid"))

        # 🔥 SAVE NGAY
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump({
                "fb_accounts": self.fb_accounts,
                "golike_token": self.golike_token,
                "job_config": self.job_config
            }, f, ensure_ascii=False, indent=2)

        print(f"Đã xóa {len(deleted)} acc:", deleted)
    def auto_verify_golike(self, fb_acc):
        fb = FB_API(fb_acc["cookie"])
        fb_id = str(fb_acc["uid"])

        group_id = "2412323175767156"
        post_id = "2605594273106711"

        try:
            # ===== JOIN =====
            self.table[fb_id]["status"] = " Check join..."

            if not fb.IS_JOINED_GROUP(group_id):
                self.table[fb_id]["status"] = " Đang join group..."
                fb.JOIN_GROUP(group_id)
                time.sleep(5)

            self.table[fb_id]["status"] = " Đã join group"

            # ===== LIKE =====
            self.table[fb_id]["status"] = " Check like..."

            if not fb.IS_LIKED(post_id):
                self.table[fb_id]["status"] = " Đang like..."
                fb.REACTION("LIKE", post_id)
                time.sleep(5)

            self.table[fb_id]["status"] = " Đã like"

            # ===== VERIFY =====
            self.table[fb_id]["status"] = " Đang verify..."

            res = requests.post(
                "https://gateway.golike.net/api/fb-account/verify-account",
                headers={
                    "authorization": f"{self.golike_token}"  # ✅ FIX
                },
                json={
                    "object_id": f"https://www.facebook.com/profile.php?id={fb_acc['uid']}"
                }
            )

            data = res.json()
            msg = str(data.get("message", ""))

            # ===== UPDATE TABLE =====
            if data.get("success"):
                if "chờ" in msg.lower() or "duyệt" in msg.lower():
                    self.table[fb_id]["status"] = f" Pending | {msg}"
                else:
                    self.table[fb_id]["status"] = f" Verify OK | {msg}"
            else:
                self.table[fb_id]["status"] = f" Verify Fail | {msg}"

            return {
                "success": data.get("success", False),
                "message": msg
            }

        except Exception as e:
            self.table[fb_id]["status"] = f" Verify Error | {str(e)[:50]}"
            return {"success": False, "message": str(e)}
    def choose_job_config(self):
        print("\n===== CẤU HÌNH JOB =====")
        print("1. Reaction (full cảm xúc)")
        print("2. Follow")
        print("3. Comment")
        print("Nhập: 1,2,3 hoặc all")

        print(f"Config hiện tại: {self.job_config}")
        use_old = input("Dùng config này? (y/n): ").lower().strip()

        # ✅ dùng config cũ
        if use_old == "y":
            print("Dùng config cũ")
            return

        # ❌ tạo config mới
        print("Nhập cấu hình mới:")

        map_job = {
            "1": "reaction",
            "2": "follow",
            "3": "review"
        }

        # 🔥 LOOP nhập cho đúng
        while True:
            inp = input("Chọn job: ").lower().strip()

            if inp == "all":
                types = ["all"]
                break

            types = []
            for x in inp.split(","):
                x = x.strip()
                if x in map_job:
                    types.append(map_job[x])

            if types:
                break  # ✅ hợp lệ

            print(" Không hợp lệ, nhập lại (vd: 1,2 hoặc all)")

        # =========================
        # nhập số job
        # =========================
        while True:
            try:
                max_jobs = int(input("Số job tối đa: "))
                if max_jobs > 0:
                    break
                else:
                    print(" Phải > 0")
            except:
                print(" Nhập số hợp lệ")

        # 🔥 lưu config mới
        self.job_config = {
            "max_jobs": max_jobs,
            "types": types
        }

        self.save_data()

        print(f" Config mới: {self.job_config}")
    def login_simple(self):
        print("===== LOGIN UID | PASS =====")

        uid = input("UID / Email / SĐT: ").strip()
        password = input("Password: ").strip()
        tfa = input("2FA (nếu có - enter bỏ qua): ").strip().replace(" ", "")
        machine_id = input("Machine ID (enter bỏ qua): ").strip() or None

        fb = FacebookLogin(
            uid_phone_mail=uid,
            password=password,
            twwwoo2fa=tfa,
            machine_id=machine_id,
            convert_all_tokens=False
        )

        result = fb.login()

        # ===== FAIL =====
        if not result.get("success"):
            print("❌ LOGIN FAIL:", result.get("error"))
            return

        # ===== SUCCESS =====
        print("✅ LOGIN SUCCESS")

        user_token = result["original_token"]["access_token"]
        cookie = result["cookies"]["string"]

        # ===== GET INFO =====
        try:
            r = requests.get(
                "https://graph.facebook.com/me",
                params={"access_token": user_token},
                timeout=10
            ).json()

            uid_real = r.get("id", uid)
            name = r.get("name", "Unknown")

        except:
            uid_real = uid
            name = "Unknown"

        # ===== SAVE =====
        self.fb_accounts.append({
            "uid": uid_real,
            "name": name,
            "cookie": cookie,
            "token": user_token,
            "pages": []  # để trống
        })

        self.save_data()

        print(f"{name} | {uid_real}")     
    def choose_mode(self):
        print("1. Cookie (full)")
        print("2. Token (reaction only)")
        c = input("Chọn: ")

        if c == "2":
            self.run_mode = "token"
        else:
            self.run_mode = "cookie"

        print("Mode:", self.run_mode)   
    def convert_pfbid(self, link):
        if link in self.pfbid_cache:
            return self.pfbid_cache[link]

        try:
            # ép link sạch
            link = link.strip()

            url = "https://id.traodoisub.com/api.php"

            res = requests.post(
                url,
                data={"link": link},
                headers={
                    "user-agent": "Mozilla/5.0",
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://id.traodoisub.com",
                    "referer": "https://id.traodoisub.com/"
                },
                timeout=10
            )

            js = res.json()
            # print("CONVERT DEBUG:", js)

            post_id = None

            # ===== CASE 1 =====
            if isinstance(js, dict):
                post_id = js.get("post_id") or js.get("id")

                # ===== CASE 2 =====
                if not post_id and "data" in js:
                    post_id = js["data"].get("id") or js["data"].get("post_id")

                # ===== CASE 3 (string fallback) =====
                if not post_id and "message" in js:
                    import re
                    m = re.search(r"\d{5,}", js["message"])
                    if m:
                        post_id = m.group()

            # ===== FINAL CLEAN =====
            if post_id:
                post_id = str(post_id)

                self.pfbid_cache[link] = post_id
                return post_id

        except Exception as e:
            print(" convert lỗi:", e)

        return None
    def load_accounts_from_file(self):
        file_name = "accounts_fb.txt"

        if not os.path.exists(file_name):
            print("❌ Không tìm thấy file accounts_fb.txt")
            return

        new_indexes = []

        # =========================
        # 🔥 AUTO FIND COOKIE
        # =========================
        def find_cookie(parts):
            for p in parts:
                p = p.strip()
                if "c_user=" in p and "xs=" in p:
                    return p
            return None

        # =========================
        # 🔥 AUTO FIND TOKEN
        # =========================
        def find_token(parts):
            for p in parts:
                p = p.strip()
                if p.startswith("EA") and len(p) > 100:
                    return p
            return None

        # =========================
        # 🔥 AUTO FIND PROXY (SIÊU TRÂU)
        # =========================
        def find_proxy(parts):
            for p in parts[::-1]:  # 🔥 quét từ cuối
                p = p.strip()

                if not p:
                    continue

                # ❌ bỏ cookie
                if "c_user=" in p or "xs=" in p:
                    continue

                # ❌ bỏ token
                if p.startswith("EA"):
                    continue

                # ❌ bỏ email
                if "@" in p and ":" not in p:
                    continue

                # ✅ ip:port
                if re.match(r"^\d{1,3}(\.\d{1,3}){3}:\d+$", p):
                    return p

                # ✅ domain/ip:port:user:pass
                if re.match(r"^[^|:]+:\d+:[^:]+:[^:]+$", p):
                    return p

                # ✅ domain:port
                if re.match(r"^[\w\.-]+:\d+$", p):
                    return p

            return None

        # =========================
        # 🔥 FORMAT PROXY
        # =========================
        def format_proxy(proxy):
            if not proxy:
                return None

            try:
                proxy = proxy.replace("http://", "").replace("https://", "")

                parts = proxy.split(":")

                # ip/domain:port:user:pass
                if len(parts) == 4:
                    host, port, user, password = parts
                    proxy_url = f"http://{user}:{password}@{host}:{port}"

                # ip/domain:port
                elif len(parts) == 2:
                    host, port = parts
                    proxy_url = f"http://{host}:{port}"

                else:
                    return None

                return {
                    "http": proxy_url,
                    "https": proxy_url
                }

            except:
                return None

        # =========================
        # 🔥 READ FILE
        # =========================
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            parts = line.split("|")

            cookie = find_cookie(parts)
            token = find_token(parts)
            raw_proxy = find_proxy(parts)
            proxy = format_proxy(raw_proxy)

            # 🔥 DEBUG (rất quan trọng)
            print("\n========================")
            print("LINE:", line)
            print("COOKIE:", cookie)
            print("TOKEN:", token)
            print("RAW PROXY:", raw_proxy)
            print("FORMAT PROXY:", proxy)

            if not cookie or not token:
                print("❌ Thiếu cookie/token → bỏ")
                continue

            self.fb_accounts.append({
                "cookie": cookie,
                "token": token,
                "proxy": proxy,
                "new": True
            })

            new_indexes.append(len(self.fb_accounts) - 1)

        print(f"\n🚀 Đã load {len(new_indexes)} acc → bắt đầu check...\n")

        if new_indexes:
            self.check_cookies(auto_select=new_indexes)
# ================= MAIN =================
if __name__ == "__main__":
    AppCLI().menu()


