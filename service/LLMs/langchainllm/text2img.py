import os.path
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import dashscope
from config.apiconfig import FIGURE_PATH

def simple_call(prompt, APIKEY, userid):

    dashscope.api_key = APIKEY
    rsp = ImageSynthesis.call(model=ImageSynthesis.Models.wanx_v1,
                              prompt=prompt,
                              n=1,
                              size='1024*1024')
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        # save file to current directory
        for result in rsp.output.results:
            with open(os.path.join(FIGURE_PATH, f"{userid}.png"), 'wb+') as f:
                f.write(requests.get(result.url).content)
        return "Finish"
    else:
        return 'Failed, status_code: %s, code: %s, message: %s' %(rsp.status_code, rsp.code, rsp.message)