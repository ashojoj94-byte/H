import os
import streamlit as st
from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI

# إعداد واجهة التطبيق
st.set_page_config(
    page_title="غرفة عمليات التداول متعددة الوكلاء",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 نظام التداول الذكي متعدد الوكلاء (Multi-Agent Trading System)")
st.markdown(
    "نظام تحليلي متكامل موزع على ثلاثة عقول رئيسية (إدارة المخاطر، التحليل الاستراتيجي، وتنفيذ الصفقات) والوكلاء التسعة."
)

# الشريط الجانبي للإعدادات
with st.sidebar:
    st.header("⚙️ إعدادات غرفة العمليات")
    openai_api_key = st.text_input("أدخل مفتاح OpenAI API Key:", type="password")

    asset_choice = st.selectbox(
        "اختر الأصل المالي للتحليل:",
        ["الذهب (XAU/USD)", "مؤشر SPX", "مؤشر NDX", "الأسهم القيادية"],
    )

    market_status = st.selectbox(
        "حالة السوق الحالية:", ["مغلق (عطلة أسبوعية)", "مفتوح (تداول حي)"]
    )

    current_price = st.text_input(
        "السعر الحالي / آخر إغلاق:", "4348.00"
    )

    analysis_button = st.button("🚀 تشغيل العقول وتحليل السوق")

# الشاشة الرئيسية
if analysis_button:
    if not openai_api_key:
        st.error("الرجاء إدخال مفتاح OpenAI API Key في الشريط الجانبي أولاً.")
    else:
        with st.spinner(
            "جاري تنسيق العمل بين العقول الثلاثة والوكلاء التسعة لتحليل السوق..."
        ):
            try:
                # إعداد النموذج
                llm = ChatOpenAI(
                    model="gpt-4o", temperature=0.2, openai_api_key=openai_api_key
                )

                # ==========================================
                # 🧠 العقل الأول: مخ إدارة المخاطر
                # ==========================================
                risk_manager = Agent(
                    role="مدير المخاطر الرئيسي",
                    goal="حماية رأس المال وتحديد حجم العقد ونسب المخاطرة بدقة.",
                    backstory="خبير مخضرم في إدارة المخاطر المالية وحماية الحسابات من التقلبات العنيفة.",
                    verbose=False,
                    llm=llm,
                )

                trade_guardian = Agent(
                    role="وكيل الصفقات (Trade Guardian)",
                    goal="مراقبة الصفقات ومتابعة نقاط الخروج وتحريك وقف الخسارة.",
                    backstory="مراقب آلي دقيق لضمان تأمين الأرباح في الوقت المناسب.",
                    verbose=False,
                    llm=llm,
                )

                # ==========================================
                # 🧠 العقل الثاني: مخ التحليل الاستراتيجي
                # ==========================================
                path_analyst = Agent(
                    role="محلل المسارات",
                    goal="تحديد الاتجاه العام (Trend) ومناطق السيولة والسيناريوهات البديلة.",
                    backstory="محلل فني يقرأ الهيكل السعري ويحدد الدعوم والمقاومات الكبرى.",
                    verbose=False,
                    llm=llm,
                )

                performance_analyst = Agent(
                    role="محلل الأداء",
                    goal="تقييم كفاءة التداول ونسبة العائد إلى المخاطر.",
                    backstory="محلل إحصائي يقيس جودة الصفقات وسجل الأداء.",
                    verbose=False,
                    llm=llm,
                )

                # ==========================================
                # 🧠 العقل الثالث: مخ تنفيذ الصفقات والأصول
                # ==========================================
                gold_agent = Agent(
                    role="وكيل الأصول والذهب",
                    goal="تتبع حركة السعر والارتباطات الخاصة بالأصل المحدد.",
                    backstory="خبير في تتبع سلوك السيولة للأصل المستهدف.",
                    verbose=False,
                    llm=llm,
                )

                execution_agent = Agent(
                    role="وكيل التداول التنفيذي",
                    goal="صياغة القرار النهائي المتكامل للتنفيذ.",
                    backstory="منفذ صفقات محترف يتمتع بدقة متناهية.",
                    verbose=False,
                    llm=llm,
                )

                # المهام الموزعة بدقة على الوكلاء
                task1 = Task(
                    description=f"قم بتحليل المسار الفني والاتجاه لـ {asset_choice} عند السعر {current_price} مع مراعاة أن حالة السوق هي: {market_status}.",
                    expected_output="تقرير فني شامل يحدد الاتجاه العام ومناطق السيولة.",
                    agent=path_analyst,
                )

                task2 = Task(
                    description="بناءً على تقرير التحليل الاستراتيجي، قم بوضع استراتيجية إدارة مخاطر محكمة تتضمن وقف الخسارة، الأهداف، وحجم المخاطرة الآمن.",
                    expected_output="خطة إدارة مخاطر دقيقة متضمنة نقاط الحماية.",
                    agent=risk_manager,
                )

                task3 = Task(
                    description="بناءً على مخرجات التحليل وإدارة المخاطر، قم بصياغة التوصية التنفيذية النهائية (شراء / بيع / انتظار) بدقة تامة.",
                    expected_output="قرار تنفيذي نهائي مفصل للمتداول.",
                    agent=execution_agent,
                )

                # إنشاء فريق العمل (Crew)
                trading_crew = Crew(
                    agents=[
                        path_analyst,
                        gold_agent,
                        risk_manager,
                        trade_guardian,
                        performance_analyst,
                        execution_agent,
                    ],
                    tasks=[task1, task2, task3],
                    process=Process.sequential,
                    verbose=False,
                )

                # تنفيذ العمليات
                result = trading_crew.kickoff()

                st.success(
                    "✅ تم إتمام التحليل الشامل عبر العقول الثلاثة بنجاح!"
                )

                # عرض النتائج في واجهة منسقة
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 🧠 تقرير العقول والوكلاء")
                    st.write(result)

                with col2:
                    st.markdown("### 📊 ملخص القرار التنفيذي")
                    st.info(
                        f"**الأصل:** {asset_choice}\n\n**السعر المرجعي:** {current_price}\n\n**حالة النظام:** جاهز ومستقر للتشغيل الحي."
                    )

            except Exception as e:
                st.error(f"حدث خطأ أثناء تشغيل النظام: {e}")
else:
    st.info(
        "👈 يرجى إدخال مفتاح الـ API في الشريط الجانبي واختيار الأصل ثم الضغط على زر **'تشغيل العقول وتحليل السوق'** لبدء الجلسة."
    )
