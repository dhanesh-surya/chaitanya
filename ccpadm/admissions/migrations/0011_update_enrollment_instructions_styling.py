# Generated manually for updating EnrollmentInstruction with modern academic styling and icons
from django.db import migrations


def update_instructions(apps, schema_editor):
    EnrollmentInstruction = apps.get_model('admissions', 'EnrollmentInstruction')

    html_content = """<div class="enrollment-steps-container">
    <div class="step-card step-card--1">
        <div class="step-card-header">
            <span class="step-number-badge"><i class="fas fa-right-to-bracket" aria-hidden="true"></i> चरण 1</span>
            <h4 class="step-heading">पोर्टल पर जाना और लॉगिन करना</h4>
        </div>
        <div class="step-card-body">
            <ol>
                <li>अपने मोबाइल या कंप्यूटर के ब्राउज़र में <strong>online.chaitanyacg.ac.in</strong> खोलें।</li>
                <li>होमपेज पर <strong>Student Login</strong> बटन पर क्लिक करें।</li>
                <li>अपना <strong>Registration No.</strong> (पंजीकरण क्रमांक) और <strong>Password</strong> (पासवर्ड) दर्ज करके लॉगिन करें।</li>
            </ol>
            <div class="step-alert-box info">
                <i class="fas fa-info-circle"></i> <div><strong>नोट:</strong> यदि पासवर्ड भूल गए हैं, तो "Forgot Password" पर क्लिक करके अपना नाम, जन्मतिथि और आधार नंबर डालकर तुरंत पासवर्ड प्राप्त कर सकते हैं।</div>
            </div>
        </div>
    </div>

    <div class="step-card step-card--2">
        <div class="step-card-header">
            <span class="step-number-badge"><i class="fas fa-file-pen" aria-hidden="true"></i> चरण 2</span>
            <h4 class="step-heading">नामांकन (Enrollment) फॉर्म खोलना</h4>
        </div>
        <div class="step-card-body">
            <ol>
                <li>लॉगिन करने के बाद आपका <strong>Student Dashboard</strong> खुल जाएगा।</li>
                <li>डैशबोर्ड पर दिए गए <strong>"Apply for Enrollment"</strong> या <strong>"Complete Enrollment"</strong> बटन पर क्लिक करें।</li>
            </ol>
        </div>
    </div>

    <div class="step-card step-card--3">
        <div class="step-card-header">
            <span class="step-number-badge"><i class="fas fa-user-check" aria-hidden="true"></i> चरण 3</span>
            <h4 class="step-heading">अपनी जानकारी और विषय (Subjects) का सत्यापन</h4>
        </div>
        <div class="step-card-body">
            <ol>
                <li><strong>व्यक्तिगत विवरण:</strong> स्क्रीन पर आपके प्रवेश (Admission) के समय भरी गई जानकारी दिखाई देगी—जैसे आपका नाम, पिता का नाम, माता का नाम, जन्मतिथि, मोबाइल नंबर, आधार नंबर तथा आपका <strong>Applied Program</strong> (जैसे B.A. / B.Sc. / B.Com. आदि)। इसे अच्छी तरह जांच लें।</li>
                <li><strong>विषय चयन:</strong> अपने पाठ्यक्रम के अनुसार निर्धारित अनिवार्य एवं ऐच्छिक विषय (Course / Subjects) चुन लें।</li>
            </ol>
        </div>
    </div>

    <div class="step-card step-card--4">
        <div class="step-card-header">
            <span class="step-number-badge"><i class="fas fa-qrcode" aria-hidden="true"></i> चरण 4</span>
            <h4 class="step-heading">नामांकन शुल्क ₹500 का भुगतान (PNB QR कोड द्वारा)</h4>
        </div>
        <div class="step-card-body">
            <ol>
                <li>फॉर्म में नीचे <strong>Enrollment Fee: ₹500</strong> का सेक्शन दिखाई देगा।</li>
                <li>वहाँ दिए गए <strong>"Click to Pay (Scan PNB QR Code)"</strong> बटन पर क्लिक करें।</li>
                <li>स्क्रीन पर कॉलेज का आधिकारिक पंजाब नेशनल बैंक (PNB) QR कोड खुलेगा:
                    <ul class="sub-list">
                        <li><strong>मर्चेंट नाम:</strong> Principal Chaitanya Science and Arts College, Pamgarh</li>
                        <li><strong>UPI ID:</strong> <code>9827194555m@pnb</code></li>
                    </ul>
                </li>
                <li>अपने किसी भी UPI ऐप (PhonePe, Google Pay, Paytm, आदि) से इस QR कोड को स्कैन करके <strong>₹500</strong> का भुगतान करें।</li>
            </ol>
            <div class="step-alert-box warning">
                <i class="fas fa-exclamation-triangle"></i> <div><strong>जरूरी:</strong> भुगतान सफल होने के बाद स्क्रीनशॉट (Screenshot) ले लें या रसीद सेव कर लें।</div>
            </div>
        </div>
    </div>

    <div class="step-card step-card--5">
        <div class="step-card-header">
            <span class="step-number-badge"><i class="fas fa-receipt" aria-hidden="true"></i> चरण 5</span>
            <h4 class="step-heading">ट्रांजेक्शन आईडी भरना और रसीद अपलोड करना</h4>
        </div>
        <div class="step-card-body">
            <ol>
                <li>भुगतान पूरा होने के बाद वापस पोर्टल स्क्रीन पर आएँ।</li>
                <li><strong>Transaction ID / UTR Number</strong> वाले बॉक्स में अपने पेमेंट का 12 अंकों का UTR नंबर या ट्रांजेक्शन आईडी दर्ज करें।</li>
                <li><strong>Upload Payment Receipt</strong> विकल्प पर क्लिक करके अपने पेमेंट स्क्रीनशॉट की फ़ोटो (या PDF) अपलोड करें।</li>
            </ol>
        </div>
    </div>

    <div class="step-card step-card--6">
        <div class="step-card-header">
            <span class="step-number-badge"><i class="fas fa-circle-check" aria-hidden="true"></i> चरण 6</span>
            <h4 class="step-heading">फ़ोटो, हस्ताक्षर और फाइनल सबमिट (Final Submit)</h4>
        </div>
        <div class="step-card-body">
            <ol>
                <li>अपना फ़ोटो और हस्ताक्षर (Signature) चेक कर लें।</li>
                <li>सभी विवरण सही होने की पुष्टि करने के बाद नीचे दिए गए <strong>"Submit Enrollment Form"</strong> बटन पर क्लिक करें।</li>
                <li>फॉर्म सबमिट होते ही आपका नामांकन दर्ज हो जाएगा और आपका <strong>Enrollment Number</strong> जारी हो जाएगा।</li>
            </ol>
        </div>
    </div>

    <div class="step-card step-card--7">
        <div class="step-card-header">
            <span class="step-number-badge"><i class="fas fa-print" aria-hidden="true"></i> चरण 7</span>
            <h4 class="step-heading">नामांकन फॉर्म और रसीद का प्रिंट निकालना</h4>
        </div>
        <div class="step-card-body">
            <ol>
                <li>फॉर्म सबमिट होने के बाद स्क्रीन पर <strong>Print Slip</strong> और <strong>Payment Receipt</strong> का विकल्प दिखाई देगा।</li>
                <li>नामांकन फॉर्म (Enrollment Slip) और ₹500 की फीस रसीद (Payment Receipt) दोनों का साफ़ प्रिंटआउट (A4 साइज़) निकाल लें।</li>
            </ol>
        </div>
    </div>

    <div class="step-card step-card--8">
        <div class="step-card-header">
            <span class="step-number-badge"><i class="fas fa-building-columns" aria-hidden="true"></i> चरण 8</span>
            <h4 class="step-heading">कॉलेज कार्यालय (Office) में अंतिम जमा करना</h4>
        </div>
        <div class="step-card-body">
            <p><strong>प्रिंटआउट लेने के बाद निम्नलिखित दस्तावेज़ों का एक सेट तैयार करें:</strong></p>
            <ol>
                <li>नामांकन फॉर्म का प्रिंटआउट (छात्र एवं पालक के हस्ताक्षर सहित)</li>
                <li>₹500 ऑनलाइन भुगतान रसीद की प्रति (Transaction ID / UTR वाली)</li>
                <li>10वीं एवं 12वीं की अंकसूची की स्व-प्रमाणित छायाप्रति (Photocopy)</li>
                <li>स्थानांतरण प्रमाण पत्र (TC) एवं चरित्र प्रमाण पत्र (CC) मूल प्रति (यदि पहले जमा न किया गया हो)</li>
                <li>आधार कार्ड की छायाप्रति</li>
                <li>जाति एवं निवास प्रमाण पत्र की छायाप्रति (आरक्षित वर्ग के लिए)</li>
            </ol>
            <div class="step-alert-box success">
                <i class="fas fa-check-circle"></i> <div>इन सभी दस्तावेज़ों को एक साथ नत्थी (Staple) करके चैतन्य कॉलेज के <strong>कार्यालय (Office / Enrollment Counter)</strong> में निर्धारित अंतिम तिथि से पहले जमा करें तथा कार्यालय से अपनी पावती (Seal / Signature) अवश्य प्राप्त करें।</div>
            </div>
        </div>
    </div>
</div>"""

    EnrollmentInstruction.objects.update_or_create(
        id=1,
        defaults={
            'college_title': 'चैतन्य साइंस एंड आर्ट्स कॉलेज, पामगढ़',
            'title': 'छात्र नामांकन (Enrollment) प्रक्रिया — चरण-दर-चरण निर्देश',
            'content_html': html_content,
            'is_active': True,
        }
    )


def reverse_update(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0010_seed_enrollment_instructions'),
    ]

    operations = [
        migrations.RunPython(update_instructions, reverse_code=reverse_update),
    ]
