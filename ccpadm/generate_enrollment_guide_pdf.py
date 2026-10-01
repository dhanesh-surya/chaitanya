"""
Script to generate a pristine, 4-page publication-ready Student Enrollment Guidance PDF.
"""

import os
from xhtml2pdf import pisa
import pypdf

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Student Online Enrollment Guide - Chaitanya College</title>
    <style>
        @page {
            size: a4 portrait;
            margin: 10mm 12mm 10mm 12mm;
        }

        body {
            font-family: Helvetica, Arial, sans-serif;
            color: #1e293b;
            font-size: 8.5pt;
            line-height: 1.35;
            margin: 0;
            padding: 0;
        }

        h1, h2, h3, h4, p {
            margin: 0;
            padding: 0;
        }

        .header-table {
            width: 100%;
            border-bottom: 2pt solid #800000;
            padding-bottom: 4pt;
            margin-bottom: 6pt;
        }

        .college-title {
            font-size: 15pt;
            font-weight: bold;
            color: #800000;
            text-align: center;
            letter-spacing: 0.5pt;
            text-transform: uppercase;
        }

        .college-sub {
            font-size: 8pt;
            color: #082b49;
            text-align: center;
            font-weight: bold;
            margin-top: 1pt;
        }

        .college-meta {
            font-size: 7.5pt;
            color: #475569;
            text-align: center;
            margin-top: 1pt;
        }

        .naac-badge {
            color: #b8860b;
            font-weight: bold;
            font-size: 8pt;
        }

        .doc-title-bar {
            background-color: #082b49;
            color: #ffffff;
            text-align: center;
            padding: 5pt 8pt;
            margin-top: 4pt;
            margin-bottom: 7pt;
        }

        .doc-title {
            font-size: 11pt;
            font-weight: bold;
            letter-spacing: 0.5pt;
            text-transform: uppercase;
        }

        .doc-subtitle {
            font-size: 8pt;
            color: #93c5fd;
            margin-top: 2pt;
        }

        .section-header {
            background-color: #f1f5f9;
            border-left: 3pt solid #800000;
            padding: 3pt 6pt;
            font-size: 9.5pt;
            font-weight: bold;
            color: #082b49;
            margin-top: 7pt;
            margin-bottom: 5pt;
            text-transform: uppercase;
        }

        .workflow-table {
            width: 100%;
            margin-bottom: 7pt;
            border-collapse: collapse;
        }

        .step-box {
            background-color: #ffffff;
            border: 0.8pt solid #cbd5e1;
            padding: 4pt 3pt;
            text-align: center;
            vertical-align: top;
        }

        .step-num {
            background-color: #800000;
            color: #ffffff;
            font-weight: bold;
            font-size: 7pt;
            padding: 1pt 4pt;
            display: inline-block;
            margin-bottom: 2pt;
        }

        .step-title {
            font-weight: bold;
            font-size: 7.5pt;
            color: #082b49;
            margin-bottom: 1pt;
        }

        .step-desc {
            font-size: 6.8pt;
            color: #64748b;
            line-height: 1.2;
        }

        .arrow-cell {
            text-align: center;
            vertical-align: middle;
            font-size: 10pt;
            color: #800000;
            font-weight: bold;
            width: 10pt;
        }

        .info-card {
            background-color: #f8fafc;
            border: 0.8pt solid #e2e8f0;
            border-left: 2.5pt solid #0284c7;
            padding: 5pt 7pt;
            margin-bottom: 6pt;
        }

        .warning-card {
            background-color: #fffbeb;
            border: 0.8pt solid #fef3c7;
            border-left: 2.5pt solid #d97706;
            padding: 5pt 7pt;
            margin-bottom: 6pt;
        }

        .success-card {
            background-color: #f0fdf4;
            border: 0.8pt solid #dcfce7;
            border-left: 2.5pt solid #16a34a;
            padding: 5pt 7pt;
            margin-bottom: 6pt;
        }

        .danger-card {
            background-color: #fef2f2;
            border: 0.8pt solid #fee2e2;
            border-left: 2.5pt solid #dc2626;
            padding: 5pt 7pt;
            margin-bottom: 6pt;
        }

        .card-title {
            font-weight: bold;
            font-size: 8.5pt;
            margin-bottom: 2pt;
        }

        .info-title { color: #0369a1; }
        .warning-title { color: #b45309; }
        .success-title { color: #15803d; }
        .danger-title { color: #b91c1c; }

        .card-text {
            font-size: 7.8pt;
            color: #334155;
            line-height: 1.3;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 4pt;
            margin-bottom: 6pt;
        }

        .data-table th {
            background-color: #082b49;
            color: #ffffff;
            font-size: 7.5pt;
            font-weight: bold;
            text-align: left;
            padding: 3.5pt 5pt;
            border: 0.5pt solid #082b49;
        }

        .data-table td {
            font-size: 7.5pt;
            padding: 3.5pt 5pt;
            border: 0.5pt solid #cbd5e1;
            vertical-align: top;
        }

        .data-table tr:nth-child(even) td {
            background-color: #f8fafc;
        }

        .badge {
            font-size: 7pt;
            font-weight: bold;
            padding: 1pt 3.5pt;
            border-radius: 2pt;
            display: inline-block;
        }

        .badge-code {
            background-color: #eff6ff;
            color: #1d4ed8;
            border: 0.5pt solid #bfdbfe;
            font-family: Courier, monospace;
        }

        .badge-blue {
            background-color: #e0f2fe;
            color: #0369a1;
        }

        .badge-green {
            background-color: #dcfce7;
            color: #15803d;
        }

        .badge-yellow {
            background-color: #fef3c7;
            color: #92400e;
        }

        .badge-red {
            background-color: #fee2e2;
            color: #991b1b;
        }

        .page-break {
            page-break-before: always;
        }

        .ui-mockup {
            border: 1.2pt solid #082b49;
            background-color: #ffffff;
            margin-top: 4pt;
            margin-bottom: 5pt;
        }

        .ui-mockup-header {
            background-color: #082b49;
            color: #ffffff;
            padding: 3pt 6pt;
            font-size: 7.5pt;
            font-weight: bold;
        }

        .ui-mockup-body {
            padding: 6pt;
            background-color: #f8fafc;
        }

        .checklist-item {
            font-size: 7.8pt;
            margin-bottom: 2pt;
        }

        .check-icon {
            color: #16a34a;
            font-weight: bold;
        }

        .bullet-list {
            margin: 2pt 0 4pt 10pt;
            padding: 0;
            font-size: 8pt;
        }

        .bullet-list li {
            margin-bottom: 2pt;
            line-height: 1.3;
        }

        .footer-note {
            font-size: 7pt;
            color: #64748b;
            text-align: center;
            border-top: 0.5pt solid #e2e8f0;
            padding-top: 3pt;
            margin-top: 6pt;
        }
    </style>
</head>
<body>

    <!-- ========================================== PAGE 1 ========================================== -->

    <!-- Header -->
    <table class="header-table">
        <tr>
            <td style="text-align: center;">
                <div class="college-title">Chaitanya Science and Arts College</div>
                <div class="college-sub">(An Autonomous Institution Approved by UGC)</div>
                <div class="college-meta">
                    Pamgarh, Dist - Janjgir-Champa (Chhattisgarh) &nbsp;|&nbsp; 
                    <span class="naac-badge">Accredited 'A' Grade by NAAC</span>
                </div>
                <div class="college-meta" style="color: #0b3d91;">
                    Affiliated to Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh (C.G.)
                </div>
            </td>
        </tr>
    </table>

    <!-- Title Bar -->
    <div class="doc-title-bar">
        <div class="doc-title">Student Online Enrollment Guide (सचित्र मार्गदर्शिका)</div>
        <div class="doc-subtitle">Official Step-by-Step Instructions for Applying for University Enrollment (Session 2026-27 / NEP 2020)</div>
    </div>

    <!-- 6-Step Visual Workflow -->
    <div class="section-header">1. Quick Workflow Overview (नामांकन प्रक्रिया का सचित्र क्रम)</div>
    <table class="workflow-table">
        <tr>
            <td class="step-box" style="width: 14%;">
                <div class="step-num">STEP 1</div>
                <div class="step-title">Login</div>
                <div class="step-desc">Enter Reg No &amp; Password</div>
            </td>
            <td class="arrow-cell">&rarr;</td>
            <td class="step-box" style="width: 14%;">
                <div class="step-num">STEP 2</div>
                <div class="step-title">Open Form</div>
                <div class="step-desc">Click "Apply for Enrollment"</div>
            </td>
            <td class="arrow-cell">&rarr;</td>
            <td class="step-box" style="width: 15%;">
                <div class="step-num">STEP 3</div>
                <div class="step-title">Fill &amp; Choose</div>
                <div class="step-desc">Verify Data &amp; NEP Courses</div>
            </td>
            <td class="arrow-cell">&rarr;</td>
            <td class="step-box" style="width: 15%;">
                <div class="step-num">STEP 4</div>
                <div class="step-title">Upload Docs</div>
                <div class="step-desc">Photo, Sign &amp; Marksheets</div>
            </td>
            <td class="arrow-cell">&rarr;</td>
            <td class="step-box" style="width: 14%;">
                <div class="step-num">STEP 5</div>
                <div class="step-title">Submit</div>
                <div class="step-desc">Review &amp; Final Submit</div>
            </td>
            <td class="arrow-cell">&rarr;</td>
            <td class="step-box" style="width: 15%;">
                <div class="step-num">STEP 6</div>
                <div class="step-title">Print Slip</div>
                <div class="step-desc">Print Slip &amp; Fee Receipt</div>
            </td>
        </tr>
    </table>

    <!-- Prerequisites -->
    <div class="info-card">
        <div class="card-title info-title">&#9432; Prerequisites Before You Begin (आवेदन से पूर्व आवश्यक सामग्री)</div>
        <div class="card-text">
            Keep the following ready before starting your online enrollment application:
            <table style="width: 100%; margin-top: 3pt;">
                <tr>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> <b>Student Registration No:</b> e.g., <code>2026xxxx</code></div>
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> <b>Portal Password:</b> Created during college admission</div>
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> <b>Aadhaar Card:</b> 12-digit valid Aadhaar number</div>
                    </td>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> <b>Passport Photo:</b> Recent clear photo (&lt; 200 KB, JPG/PNG)</div>
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> <b>Student Signature:</b> On white paper (&lt; 100 KB, JPG/PNG)</div>
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> <b>10th &amp; 12th Details:</b> Roll No, Board, Marks, Year</div>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <!-- Step 1 Details -->
    <div class="section-header">2. Step 1: Student Login &amp; Password Recovery (लॉगिन एवं पासवर्ड पुनर्प्राप्ति)</div>
    <div class="card-text" style="margin-bottom: 4pt;">
        Open the student portal in your web browser: <code>http://127.0.0.1:8000/login/</code> (or official portal domain).
    </div>

    <table style="width: 100%;">
        <tr>
            <td style="width: 48%; vertical-align: top;">
                <div class="ui-mockup">
                    <div class="ui-mockup-header">A. Regular Student Portal Login</div>
                    <div class="ui-mockup-body">
                        <div style="font-size: 7.5pt; margin-bottom: 3pt;"><b>User ID / Reg No:</b> <code>20260002</code></div>
                        <div style="font-size: 7.5pt; margin-bottom: 5pt;"><b>Password:</b> <code>&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;</code></div>
                        <div style="text-align: center;">
                            <span class="badge badge-green" style="padding: 2.5pt 7pt;">[ Login to Dashboard ]</span>
                        </div>
                        <div style="margin-top: 5pt; font-size: 7pt; text-align: center; color: #0284c7;">
                            Forgot Password? Click "Forgot Password?" below the form.
                        </div>
                    </div>
                </div>
            </td>
            <td style="width: 4%;"></td>
            <td style="width: 48%; vertical-align: top;">
                <div class="ui-mockup">
                    <div class="ui-mockup-header">B. Forgot Password? (Instant Direct Retrieval)</div>
                    <div class="ui-mockup-body">
                        <div style="font-size: 7pt; color: #475569; margin-bottom: 3pt;">
                            <b>No email OTP needed!</b> Enter your 3 matching credentials:
                        </div>
                        <div style="font-size: 7pt;">1. <b>Full Name:</b> As registered during admission</div>
                        <div style="font-size: 7pt;">2. <b>Date of Birth:</b> Select your DOB</div>
                        <div style="font-size: 7pt;">3. <b>Aadhaar Number:</b> 12-digit Aadhaar (XXXX XXXX XXXX)</div>
                        <div style="text-align: center; margin-top: 4pt;">
                            <span class="badge badge-blue" style="padding: 2.5pt 6pt;">[ Verify &amp; Reveal Password ]</span>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    </table>

    <div class="success-card">
        <div class="card-title success-title">&#10004; Smart Name Matching in Password Recovery</div>
        <div class="card-text">
            The portal features intelligent name matching. Whether you enter your single name, first and last name, or name in different word order, the system matches your record with your DOB and Aadhaar securely and displays your password immediately.
        </div>
    </div>

    <div class="footer-note">Page 1 &bull; Chaitanya Science &amp; Arts College &bull; Student Online Enrollment Guide</div>

    <div class="page-break"></div>

    <!-- ========================================== PAGE 2 ========================================== -->

    <!-- Step 2 Details -->
    <div class="section-header">3. Step 2: Dashboard Overview &amp; Application Status Badges</div>
    <div class="card-text" style="margin-bottom: 4pt;">
        After logging in, your <b>Student Dashboard</b> (<code>/dashboard/</code>) displays your profile, admission status, and enrollment action card:
    </div>

    <table class="data-table">
        <tr>
            <th style="width: 25%;">Dashboard Status</th>
            <th style="width: 38%;">Action Button Displayed</th>
            <th style="width: 37%;">What You Should Do</th>
        </tr>
        <tr>
            <td><span class="badge badge-yellow">Not Started / Draft</span></td>
            <td><b>[ Apply for Enrollment ]</b> or <b>[ Edit Enrollment ]</b></td>
            <td>Click to open the online enrollment form and fill in your details.</td>
        </tr>
        <tr>
            <td><span class="badge badge-blue">Submitted / Pending Approval</span></td>
            <td><b>[ Cancel Enrollment ]</b> &nbsp;|&nbsp; <b>[ Print Slip ]</b></td>
            <td>Form submitted; waiting for admin review. You can cancel and edit if needed!</td>
        </tr>
        <tr>
            <td><span class="badge badge-green">Approved / Enrolled</span></td>
            <td><span class="badge badge-green">&#128274; Enrollment Accepted (Locked)</span></td>
            <td>Admin has approved your enrollment! Download your Print Slip &amp; Fee Receipt.</td>
        </tr>
    </table>

    <!-- Step 3 Details: Form Breakdown -->
    <div class="section-header">4. Step 3: Completing the Enrollment Form (Sections A, B &amp; C)</div>
    <table class="data-table">
        <tr>
            <th style="width: 22%;">Form Section</th>
            <th style="width: 44%;">Field Details</th>
            <th style="width: 34%;">Important Instructions</th>
        </tr>
        <tr>
            <td><b>Section A<br/>Personal &amp; Admission</b></td>
            <td>
                &bull; Full Name, Father's Name, Mother's Name<br/>
                &bull; Gender (Male / Female), Category (GEN / OBC / SC / ST)<br/>
                &bull; Medium of Instruction (Hindi / English)<br/>
                &bull; Admission Application / Reg Number
            </td>
            <td>
                <b>Auto-populated:</b> Data is pre-loaded from your admission form. Verify spelling against your 10th marksheet.
            </td>
        </tr>
        <tr>
            <td><b>Section B<br/>Contact &amp; Address</b></td>
            <td>
                &bull; 10-digit Active Mobile Number &amp; Email ID<br/>
                &bull; 12-digit Aadhaar Card Number<br/>
                &bull; Date of Birth (DD/MM/YYYY)<br/>
                &bull; Permanent &amp; Correspondence Address (Village, Post, Dist, Pin)
            </td>
            <td>
                Ensure mobile number and address are active, as exam roll numbers and university updates are dispatched here.
            </td>
        </tr>
        <tr>
            <td><b>Section C<br/>Previous Academic Records</b></td>
            <td>
                &bull; <b>High School (10th):</b> Roll No, Board, Year, Max &amp; Obtained Marks, %.<br/>
                &bull; <b>Intermediate (12th):</b> Roll No, Board, Year, Stream, Marks, %.
            </td>
            <td>
                Marks, roll numbers, and percentages must match your original board marksheets exactly.
            </td>
        </tr>
    </table>

    <!-- NEP Subject Selection -->
    <div class="section-header">5. Step 3 (Continued): NEP 2020 Subject &amp; Course Code Selection</div>
    
    <div class="info-card">
        <div class="card-title info-title">&#9733; NEP Subject Structure, Course Codes &amp; Default Paper No. I</div>
        <div class="card-text">
            Under NEP 2020, courses are categorized as Major, Minor, Multidisciplinary, AEC, SEC, and VAC. 
            The system clearly displays the official <b>Course Code</b> (e.g. <code>HNSC-01</code>) and assigns <b>Paper No. I</b> by default for first-semester courses.
        </div>
    </div>

    <table class="data-table">
        <tr>
            <th style="width: 15%;">Course Code</th>
            <th style="width: 25%;">Category / Type</th>
            <th style="width: 38%;">Example Subject &amp; Description</th>
            <th style="width: 22%;">Paper &amp; Credits</th>
        </tr>
        <tr>
            <td><span class="badge badge-code">HNSC-01</span></td>
            <td>Major Subject (Core I)</td>
            <td>Hindi Literature / Samajshastra / Political Science</td>
            <td>Paper I &bull; 4 Credits</td>
        </tr>
        <tr>
            <td><span class="badge badge-code">SOSC-01</span></td>
            <td>Major Subject (Core II)</td>
            <td>Sociology / Geography / History</td>
            <td>Paper I &bull; 4 Credits</td>
        </tr>
        <tr>
            <td><span class="badge badge-code">PSSC-01</span></td>
            <td>Minor Subject</td>
            <td>Political Science / Economics / Botany</td>
            <td>Paper I &bull; 4 Credits</td>
        </tr>
        <tr>
            <td><span class="badge badge-code">MDC-01</span></td>
            <td>Multidisciplinary (MDC)</td>
            <td>Introductory Interdisciplinary Course</td>
            <td>Paper I &bull; 3 Credits</td>
        </tr>
        <tr>
            <td><span class="badge badge-code">AEC-03</span></td>
            <td>Ability Enhancement (AEC)</td>
            <td>Paryavaran Adhyayan / Environmental Studies</td>
            <td>Paper I &bull; 2 Credits</td>
        </tr>
        <tr>
            <td><span class="badge badge-code">SEC-01</span></td>
            <td>Skill Enhancement (SEC)</td>
            <td>Computer Fundamentals / Communication Skills</td>
            <td>Paper I &bull; 3 Credits</td>
        </tr>
        <tr>
            <td><span class="badge badge-code">VAC-01</span></td>
            <td>Value Added Course (VAC)</td>
            <td>Yoga &amp; Health / Indian Culture &amp; Values</td>
            <td>Paper I &bull; 2 Credits</td>
        </tr>
    </table>

    <div class="warning-card">
        <div class="card-title warning-title">&#9888; Compulsory vs Elective Subjects</div>
        <div class="card-text">
            Compulsory subjects (such as Foundation and Environmental Studies) are pre-checked and locked by the system. For elective combinations, select the exact subjects allotted to you during admission.
        </div>
    </div>

    <div class="footer-note">Page 2 &bull; Chaitanya Science &amp; Arts College &bull; Student Online Enrollment Guide</div>

    <div class="page-break"></div>

    <!-- ========================================== PAGE 3 ========================================== -->

    <!-- Step 4 Details: Documents -->
    <div class="section-header">6. Step 4: Uploading Mandatory Documents (दस्तावेज अपलोड)</div>
    <table class="data-table">
        <tr>
            <th style="width: 26%;">Document Required</th>
            <th style="width: 18%;">Format</th>
            <th style="width: 18%;">Size Limit</th>
            <th style="width: 38%;">Upload Specifications</th>
        </tr>
        <tr>
            <td><b>Passport Size Photograph</b></td>
            <td>JPG / PNG</td>
            <td>Max 200 KB</td>
            <td>Clear colored photograph, light background, face clearly visible.</td>
        </tr>
        <tr>
            <td><b>Student Signature</b></td>
            <td>JPG / PNG</td>
            <td>Max 100 KB</td>
            <td>Clear signature on plain white paper using black or blue pen.</td>
        </tr>
        <tr>
            <td><b>10th Marksheet</b></td>
            <td>PDF / JPG</td>
            <td>Max 500 KB</td>
            <td>Clear readable scan showing student name, parents' names &amp; DOB.</td>
        </tr>
        <tr>
            <td><b>12th Marksheet</b></td>
            <td>PDF / JPG</td>
            <td>Max 500 KB</td>
            <td>Clear scan showing roll number, stream, and marks obtained.</td>
        </tr>
    </table>

    <!-- Step 5 Details: Submission -->
    <div class="section-header">7. Step 5: Review, Declaration &amp; Final Submission</div>
    <ul class="bullet-list">
        <li><b>Declaration:</b> Tick the self-declaration checkbox: <i>"I hereby declare that all the information furnished above is correct to the best of my knowledge."</i></li>
        <li><b>Save as Draft:</b> You can click <b>"Save Draft"</b> at any time to save progress and return later.</li>
        <li><b>Final Submit:</b> When all sections and files are complete, click <b>"Submit Enrollment Application"</b>.</li>
        <li><b>Enrollment Number:</b> Upon successful submission, your University Enrollment Number (e.g., <code>CCP26050002</code>) is generated and registered.</li>
    </ul>

    <!-- Cancel Enrollment Feature -->
    <div class="section-header">8. Special Feature: "Cancel Enrollment" Before Admin Approval</div>

    <div class="success-card">
        <div class="card-title success-title">&#10004; Made an Error? Self-Cancel and Correct Your Form Easily!</div>
        <div class="card-text">
            If you realize you made a typing mistake, chose the wrong subject, or uploaded the wrong photo <b>after clicking Submit</b>, 
            you can cancel and unlock your application directly from your dashboard <b>as long as the admin has not approved it yet</b>.
        </div>
    </div>

    <table style="width: 100%; border-collapse: collapse; margin-top: 4pt; margin-bottom: 6pt;">
        <tr>
            <td style="width: 48%; vertical-align: top; border: 1pt solid #cbd5e1; padding: 5pt; background-color: #f8fafc;">
                <div style="font-weight: bold; color: #16a34a; font-size: 8pt; margin-bottom: 2pt;">
                    &#9989; BEFORE Admin Approval (Cancellation Allowed):
                </div>
                <div style="font-size: 7.5pt; color: #334155; line-height: 1.3;">
                    &bull; Status shows: <b>Submitted / Pending Approval</b><br/>
                    &bull; <b>"Cancel Enrollment"</b> button is active.<br/>
                    &bull; Clicking Cancel immediately reverts form to <b>Draft</b>.<br/>
                    &bull; Correct your details, re-upload documents, and re-submit!
                </div>
            </td>
            <td style="width: 4%;"></td>
            <td style="width: 48%; vertical-align: top; border: 1pt solid #cbd5e1; padding: 5pt; background-color: #fef2f2;">
                <div style="font-weight: bold; color: #dc2626; font-size: 8pt; margin-bottom: 2pt;">
                    &#128274; AFTER Admin Approval (Strictly Locked):
                </div>
                <div style="font-size: 7.5pt; color: #334155; line-height: 1.3;">
                    &bull; Status shows: <b>Approved / Enrolled</b><br/>
                    &bull; Badge displays: <b>Enrollment Accepted (Locked)</b><br/>
                    &bull; Student cancellation is permanently disabled for security.<br/>
                    &bull; For any further edits, contact the college office directly.
                </div>
            </td>
        </tr>
    </table>

    <div class="danger-card">
        <div class="card-title danger-title">&#9888; Security Rule: Approval Lock</div>
        <div class="card-text">
            Once the college administrative section reviews and accepts your enrollment, the application is permanently locked against student modification. Ensure your details are verified before admin approval.
        </div>
    </div>

    <div class="footer-note">Page 3 &bull; Chaitanya Science &amp; Arts College &bull; Student Online Enrollment Guide</div>

    <div class="page-break"></div>

    <!-- ========================================== PAGE 4 ========================================== -->

    <!-- Step 6 Details: Printing -->
    <div class="section-header">9. Step 6: Printing Enrollment Slip &amp; Fee Receipt</div>
    <div class="card-text" style="margin-bottom: 4pt;">
        Once submitted or approved, download and print your official college enrollment documents from your dashboard:
    </div>

    <table class="data-table">
        <tr>
            <th style="width: 28%;">Document to Print</th>
            <th style="width: 32%;">Dashboard Button</th>
            <th style="width: 40%;">Description &amp; Use</th>
        </tr>
        <tr>
            <td><b>Enrollment Application Slip</b></td>
            <td><b>[ Print Slip ]</b></td>
            <td>Official A4 university format slip with college header, barcode, passport photo, selected course codes, and signature box.</td>
        </tr>
        <tr>
            <td><b>Enrollment Fee Receipt</b></td>
            <td><b>[ Fee Receipt ]</b></td>
            <td>Official fee payment receipt displaying fee breakdown, transaction ID, payment status, and verification stamp.</td>
        </tr>
    </table>

    <!-- Submission Checklist -->
    <div class="section-header">10. Physical Hardcopy Submission Checklist at College Counter</div>
    <div class="info-card">
        <div class="card-title info-title">&#128203; Documents to Attach with Printed Slip (कॉलेज काउंटर में जमा करने हेतु सूची)</div>
        <div class="card-text">
            Submit the printed enrollment packet to the college office along with self-attested photocopies of:
            <table style="width: 100%; margin-top: 3pt;">
                <tr>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> Printed &amp; Signed Enrollment Application Slip</div>
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> Printed Enrollment Fee Receipt</div>
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> Self-attested Photocopy of 10th Marksheet</div>
                    </td>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> Self-attested Photocopy of 12th Marksheet</div>
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> Self-attested Photocopy of Aadhaar Card</div>
                        <div class="checklist-item"><span class="check-icon">&#10004;</span> Original Transfer Certificate (TC) &amp; Migration (if applicable)</div>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <!-- FAQs -->
    <div class="section-header">11. Frequently Asked Questions (अक्सर पूछे जाने वाले प्रश्न)</div>
    <table class="data-table">
        <tr>
            <th style="width: 35%;">Question</th>
            <th style="width: 65%;">Answer / Resolution</th>
        </tr>
        <tr>
            <td><b>I forgot my portal password?</b></td>
            <td>Click "Forgot Password?" on login page. Enter your Full Name, DOB, and 12-digit Aadhaar number to view your password instantly.</td>
        </tr>
        <tr>
            <td><b>I submitted with the wrong subject?</b></td>
            <td>Go to your Student Dashboard. Before the admin approves, click <b>"Cancel Enrollment"</b> to unlock and re-select your subjects.</td>
        </tr>
        <tr>
            <td><b>Why is the Cancel button disabled?</b></td>
            <td>If the admin has already accepted and approved your enrollment, it is locked. Contact the college office for manual corrections.</td>
        </tr>
        <tr>
            <td><b>Can I submit the form on mobile?</b></td>
            <td>Yes, the portal is fully mobile responsive. However, we recommend a desktop or cyber cafe for uploading clear document scans and printing.</td>
        </tr>
    </table>

    <!-- Helpdesk Contact -->
    <div class="section-header">12. College Helpdesk &amp; Technical Assistance</div>
    <table style="width: 100%; border: 1pt solid #cbd5e1; background-color: #f8fafc; padding: 5pt;">
        <tr>
            <td style="font-size: 7.8pt; color: #334155; line-height: 1.4;">
                <b>College Administrative Block:</b> Chaitanya Science &amp; Arts College, Pamgarh, Dist - Janjgir-Champa (C.G.)<br/>
                <b>Counter Working Hours:</b> Monday to Saturday, 10:30 AM to 04:30 PM (Except Sundays &amp; State Holidays)<br/>
                <b>Official Website:</b> <a style="color: #0284c7; text-decoration: none;">http://chaitanyacg.ac.in</a> &nbsp;|&nbsp; 
                <b>Email:</b> info@chaitanyacg.ac.in &nbsp;|&nbsp; 
                <b>Technical Support:</b> Available at College Computer Center
            </td>
        </tr>
    </table>

    <div class="footer-note" style="margin-top: 10pt;">
        &copy; 2026 Chaitanya Science &amp; Arts College, Pamgarh. All Rights Reserved. &bull; Autonomous Institution Approved by UGC.
    </div>

</body>
</html>
"""

def generate_pdf():
    output_pdf_path = os.path.abspath("Student_Enrollment_User_Guide.pdf")
    static_docs_pdf_path = os.path.abspath(os.path.join("static", "docs", "Student_Enrollment_User_Guide.pdf"))

    print(f"Generating PDF guide: {output_pdf_path}")
    with open(output_pdf_path, "wb") as f:
        pisa_status = pisa.CreatePDF(HTML_CONTENT, dest=f)

    if pisa_status.err:
        print(f"Error generating PDF: {pisa_status.err}")
        return False

    reader = pypdf.PdfReader(output_pdf_path)
    page_count = len(reader.pages)
    print(f"Successfully generated: {output_pdf_path}")
    print(f"Total Pages: {page_count} | Size: {os.path.getsize(output_pdf_path)} bytes")

    # Also copy to static/docs/
    with open(static_docs_pdf_path, "wb") as f:
        pisa.CreatePDF(HTML_CONTENT, dest=f)
    print(f"Successfully saved to static docs: {static_docs_pdf_path}")
    return True

if __name__ == "__main__":
    generate_pdf()
