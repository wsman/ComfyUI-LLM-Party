import configparser
import json
import locale
import os

import openai

# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")

class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")
def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys


class mini_party:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "prompt": ("STRING", {"default": "input function here","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_str",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        prompt,
        model_name,
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        history= [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_str}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        output = response.choices[0].message.content
        return (output,)
    

class mini_translate:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "target_language": ("STRING", {"default": "English"}),
                "tone": ("STRING", {"default": "正式"}),
                "degree": ("INT", {"default": 5, " min": 0, "max": 10}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_str",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        target_language, 
        degree=5, 
        tone="正式",
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        sys_prompt = f"""你是一个翻译专家，请将我的输入翻译成{target_language}，语气为{tone}，语气程度为{str(degree)}。
语气程度最大为10，最小为0，数字越大语气越{tone}。当语气程度为0时，几乎不改变原文的语气，当语气程度为10时，语气会非常{tone}。
即使我的输入的语言和{target_language}相同，也请注意语气的调整，而不是返回原内容。
翻译时不要复述原文以及其他无关内容，直接返回翻译后的内容即可。注意！如果我输入的内容带有格式（例如markdown格式），请保留原格式。

如果是markdown格式的文字，有以下要求：
1. 请保留原格式，不要改变markdown格式。
2. 请不要改变markdown格式中的超链接中的()部分，但[]中的内容必须翻译。如果改变了()部分，可能会导致超链接失效。
3. HTML格式的文字，请保留原格式，不要改变HTML格式,其中会被显示在前端的文字需要翻译，而链接部分不能翻译。

从现在开始，请将以下内容翻译成{target_language}。
        """
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": input_str}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        output = response.choices[0].message.content
        return (output,)

class mini_sd_prompt:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "a girl","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("positive_prompt","negative_prompt",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        prompt,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        sys_prompt = f'''# Stable Diffusion prompt 助理

你来充当一位有艺术气息的Stable Diffusion prompt 助理。

## 任务

我用自然语言告诉你要生成的prompt的主题，你的任务是根据这个主题想象一幅完整的画面，然后转化成一份详细的、高质量的prompt，让Stable Diffusion可以生成高质量的图像。

## 背景介绍

Stable Diffusion是一款利用深度学习的文生图模型，支持通过使用 prompt 来产生新的图像，描述要包含或省略的元素。

## prompt 概念

- 完整的prompt包含“**Positive Prompt:**”和"**Negative Prompt:**"两部分。
- Positive prompt 用来描述图像，由普通常见的单词构成，使用英文半角","做为分隔符。
- negative prompt用来描述你不想在生成的图像中出现的内容。
- 以","分隔的每个单词或词组称为 tag。所以prompt和negative prompt是由系列由","分隔的tag组成的。

## () 和 [] 语法

调整关键字强度的等效方法是使用 () 和 []。 (keyword) 将tag的强度增加 1.1 倍，与 (keyword:1.1) 相同，最多可加三层。 [keyword] 将强度降低 0.9 倍，与 (keyword:0.9) 相同。

## Prompt 格式要求

你需要用以下json格式输出：
{{
"positive":"",
"negative":""
}}

下面我将说明 prompt 的生成步骤，这里的 prompt 可用于描述人物、风景、物体或抽象数字艺术图画。你可以根据需要添加合理的、但不少于5处的画面细节。

### 1. positive prompt 要求

- 你输出的 Stable Diffusion prompt 放入json字典的"positive"对应的值中。
- Positive prompt 内容包含画面主体、材质、附加细节、图像质量、艺术风格、色彩色调、灯光等部分，但你输出的 prompt 不能分段，例如类似"medium:"这样的分段描述是不需要的，也不能包含":"和"."。
- 画面主体：不简短的英文描述画面主体, 如 A girl in a garden，主体细节概括（主体可以是人、事、物、景）画面核心内容。这部分根据我每次给你的主题来生成。你可以添加更多主题相关的合理的细节。
- 对于人物主题，你必须描述人物的眼睛、鼻子、嘴唇，例如'beautiful detailed eyes,beautiful detailed lips,extremely detailed eyes and face,longeyelashes'，以免Stable Diffusion随机生成变形的面部五官，这点非常重要。你还可以描述人物的外表、情绪、衣服、姿势、视角、动作、背景等。人物属性中，1girl表示一个女孩，2girls表示两个女孩。
- 材质：用来制作艺术品的材料。 例如：插图、油画、3D 渲染和摄影。 Medium 有很强的效果，因为一个关键字就可以极大地改变风格。
- 附加细节：画面场景细节，或人物细节，描述画面细节内容，让图像看起来更充实和合理。这部分是可选的，要注意画面的整体和谐，不能与主题冲突。
- 图像质量：这部分内容开头永远要加上“(best quality,4k,8k,highres,masterpiece:1.2),ultra-detailed,(realistic,photorealistic,photo-realistic:1.37)”， 这是高质量的标志。其它常用的提高质量的tag还有，你可以根据主题的需求添加：HDR,UHD,studio lighting,ultra-fine painting,sharp focus,physically-based rendering,extreme detail description,professional,vivid colors,bokeh。
- 艺术风格：这部分描述图像的风格。加入恰当的艺术风格，能提升生成的图像效果。常用的艺术风格例如：portraits,landscape,horror,anime,sci-fi,photography,concept artists等。
- 色彩色调：颜色，通过添加颜色来控制画面的整体颜色。
- 灯光：整体画面的光线效果。

### 2. negative prompt 要求
- negative prompt部分放入json字典的"negative"对应的值中。你想要避免出现在图像中的内容都可以添加到"**Negative Prompt:**"后面。
- 任何情况下，negative prompt都要包含这段内容："nsfw,(low quality,normal quality,worst quality,jpeg artifacts),cropped,monochrome,lowres,low saturation,((watermark)),(white letters)"
- 如果是人物相关的主题，你的输出需要另加一段人物相关的 negative prompt，内容为：“skin spots,acnes,skin blemishes,age spot,mutated hands,mutated fingers,deformed,bad anatomy,disfigured,poorly drawn face,extra limb,ugly,poorly drawn hands,missing limb,floating limbs,disconnected limbs,out of focus,long neck,long body,extra fingers,fewer fingers,,(multi nipples),bad hands,signature,username,bad feet,blurry,bad body”。

### 3. 限制：
- tag 内容用英语单词或短语来描述，并不局限于我给你的单词。注意只能包含关键词或词组。
- 注意不要输出句子，不要有任何解释。
- tag数量限制40个以内，单词数量限制在60个以内。
- tag不要带引号("")。
- 使用英文半角","做分隔符。
- tag 按重要性从高到低的顺序排列。
- 我给你的主题可能是用中文描述，你给出的Positive prompt和negative prompt只用英文。
'''
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                            response_format={"type": "json_object"},
                        )
        output = response.choices[0].message.content
        output = json.loads(output)
        positive_prompt= output["positive"]
        negative_prompt=output["negative"]
        return (positive_prompt,negative_prompt,)



NODE_CLASS_MAPPINGS = {
    "mini_party": mini_party,
    "mini_translate": mini_translate,
    "mini_sd_prompt": mini_sd_prompt,
    }
# 获取系统语言
lang = locale.getdefaultlocale()[0]
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "mini_party": "迷你派对",
        "mini_translate": "迷你翻译机",
        "mini_sd_prompt": "迷你SD提示词生成器",
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "mini_party": "Mini-Party",
        "mini_translate": "Mini-Translator",
        "mini_sd_prompt": "Mini-SD Prompt Generator",
        }