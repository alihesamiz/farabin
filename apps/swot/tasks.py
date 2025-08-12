import logging

from celery import shared_task
from django.conf import settings
from google import genai
from openai import OpenAIError
from pydantic import BaseModel, ValidationError

logger = logging.getLogger("swot")


@shared_task(bind=True, rate_limit="5/m")
def generate_swot_analysis(self, instance_pk: int) -> None:
    from apps.swot.models import (  # noqa: F401
        SWOTAnalysis,
        SWOTMatrix,
    )

    class SWOTResponse(BaseModel):
        so: str
        st: str
        wo: str
        wt: str

    try:
        instance = SWOTMatrix.objects.select_related("company").get(pk=instance_pk)

        result = {
            "strength": {"key": [], "answers": []},
            "weakness": {"key": [], "answers": []},
            "opportunity": {"key": [], "answers": []},
            "threat": {"key": [], "answers": []},
        }
        swot_fields = ["strength", "weakness", "opportunity", "threat"]

        for field_name in swot_fields:
            json_data = getattr(instance, field_name)

            if not json_data:
                continue

            question_ids = []
            answers = []

            for key, value in json_data.items():
                try:
                    question_id = int(key)
                    question_ids.append(question_id)
                    answers.append(value)
                except (ValueError, TypeError):
                    continue
            result[field_name]["key"].extend(question_ids)
            result[field_name]["answers"].extend(answers)

            # match analysis_type:
            #     case "q":
            #         for id in question_ids:
            #             new_key = SWOTQuestion.objects.get(pk=id).text
            #             result[field_name]["key"] = new_key

            #     case "e":
            #         for id in question_ids:
            #             new_key = SWOTOption.objects.get(pk=id).option
            #             result[field_name]["key"] = new_key
            #     case _:
            #         ...

        logger.info(f"Creating SWOT analysis for {instance}")

        combinations_dict = {
            "so": result["strength"]["answers"] + result["opportunity"]["answers"],
            "st": result["strength"]["answers"] + result["threat"]["answers"],
            "wo": result["weakness"]["answers"] + result["opportunity"]["answers"],
            "wt": result["weakness"]["answers"] + result["threat"]["answers"],
        }

        prompt = f"""
            # تحلیل جامع SWOT به زبان فارسی

            بر اساس پارامترهای ارائه شده، یک تحلیل SWOT دقیق ایجاد کنید و خروجی را در قالب سازمان‌یافته با سرفصل‌های مربوطه ارائه دهید.

            ## پارامترهای SWOT:
            - **نقاط قوت و فرصت‌ها **(Strengths,Opportunities): {combinations_dict["so"]}
            - **نقاط قوت و تهدیدها **(Strengths,Threats): {combinations_dict["st"]}
            - **نقاط ضعف و فرصت‌ها **(Weaknesses,Opportunities): {combinations_dict["wo"]}
            - **نقاط ضعف و تهدیدها **(Weaknesses,Threats): {combinations_dict["wt"]}

            ## الزامات خروجی:

            ### **ماتریس SWOT**
            **خلاصه‌ای جامع از نقاط قوت، نقاط ضعف، فرصت‌ها و تهدیدها در قالب تحلیلی مختصر و مفید.**

            ### **استراتژی‌های SO **(نقاط قوت × فرصت‌ها)
            **توسعه استراتژی‌هایی که از نقاط قوت برای بهره‌برداری از فرصت‌ها استفاده می‌کنند.**
            - ⚫ هر استراتژی را با **نقطه سیاه** شروع کنید
            - ⚫ هر استراتژی باید **مشخص، واقع‌بینانه و متناسب با زمینه ارائه شده** باشد
            - ⚫ برای هر استراتژی یک **توضیح مختصر** ارائه دهید

            ### **استراتژی‌های ST **(نقاط قوت × تهدیدها)
            **توسعه استراتژی‌هایی که از نقاط قوت برای کاهش اثرات تهدیدها استفاده می‌کنند.**
            - ⚫ هر استراتژی را با **نقطه سیاه** شروع کنید
            - ⚫ هر استراتژی باید **مشخص، واقع‌بینانه و متناسب با زمینه ارائه شده** باشد
            - ⚫ برای هر استراتژی یک **توضیح مختصر** ارائه دهید

            ### **استراتژی‌های WO **(نقاط ضعف × فرصت‌ها)
            **توسعه استراتژی‌هایی که نقاط ضعف را با بهره‌برداری از فرصت‌ها برطرف می‌کنند.**
            - ⚫ هر استراتژی را با **نقطه سیاه** شروع کنید
            - ⚫ هر استراتژی باید **مشخص، واقع‌بینانه و متناسب با زمینه ارائه شده** باشد
            - ⚫ برای هر استراتژی یک **توضیح مختصر** ارائه دهید

            ### **استراتژی‌های WT **(نقاط ضعف × تهدیدها)
            **توسعه استراتژی‌هایی که نقاط ضعف را به حداقل رسانده و از تهدیدها اجتناب می‌کنند.**
            - ⚫ هر استراتژی را با **نقطه سیاه** شروع کنید
            - ⚫ هر استراتژی باید **مشخص، واقع‌بینانه و متناسب با زمینه ارائه شده** باشد
            - ⚫ برای هر استراتژی یک **توضیح مختصر** ارائه دهید

            **نکات مهم**:
            - ⚠️ **حتماً از فرمت نقطه‌گذاری (Bullet Points) برای شفافیت بیشتر استفاده کنید**
            - ⚠️ **متن‌های مهم را با Bold مشخص کنید**
            - ⚠️ **تمام خروجی‌ها باید به زبان فارسی و در قالب Markdown باشند**
            - ⚠️ **هر بخش را با سرفصل مناسب و سازمان‌یافته ارائه دهید**
            """
        client = genai.Client(api_key=settings.FARABIN_GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": SWOTResponse,
            },
        )
        analysis: SWOTResponse = response.parsed
        analysis_instance, _ = SWOTAnalysis.objects.get_or_create(matrix=instance)

        analysis_instance.so = analysis.so or "N/A"
        analysis_instance.st = analysis.st or "N/A"
        analysis_instance.wo = analysis.wo or "N/A"
        analysis_instance.wt = analysis.wt or "N/A"
        analysis_instance.save()

        logger.info(f"SWOT analysis created for {instance}")

    except SWOTMatrix.DoesNotExist:
        error_msg = f"CompanySWOTQuestionMatrix with id {id} does not exist."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        logger.error(
            f"Unexpected error while creating SWOT analysis for {id}: {str(e)}"
        )
        return str(e)
    except OpenAIError as genai_error:
        logger.error(f"LLM Error during content generation: {str(genai_error)}")
        raise genai_error
    except ValidationError as val_err:
        logger.error(f"Response schema validation error: {val_err}")
        raise val_err
