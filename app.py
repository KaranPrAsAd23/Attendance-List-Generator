from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    college = request.form['college']
    class_info = request.form['class']
    subject = request.form['subject']
    total_classes = int(request.form['total_classes'])

    names = request.form.getlist('name[]')
    attended = request.form.getlist('attended[]')

    data = []
    for i in range(len(names)):
        att = int(attended[i])
        percent = (att / total_classes) * 100

        data.append({
            "name": names[i],
            "attended": att,
            "percent": percent
        })

    os.makedirs("output", exist_ok=True)
    filename = "output/attendance.pdf"

    generate_pdf(data, college, class_info, subject, total_classes, filename)

    return send_file(filename, as_attachment=True)

# 🔥 FIXED PDF FUNCTION
def generate_pdf(data, college, class_info, subject, total_classes, filename):
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from datetime import datetime
    import os

    pdf = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    # 🎯 PROFESSIONAL STYLES
    title_style = ParagraphStyle(
        'title',
        fontName='Helvetica-Bold',
        fontSize=22,
        alignment=1,
        spaceAfter=10
    )

    info_style = ParagraphStyle(
        'info',
        fontName='Helvetica',
        fontSize=11,
        alignment=1,
        textColor=colors.grey,
        spaceAfter=4
    )

    summary_style = ParagraphStyle(
        'summary',
        fontName='Helvetica-Bold',
        fontSize=12,
        alignment=1,
        textColor=colors.white
    )

    footer_style = ParagraphStyle(
        'footer',
        fontName='Helvetica-Oblique',
        fontSize=9,
        alignment=1,
        textColor=colors.grey
    )

    # 📅 DATE
    date_str = datetime.now().strftime("%d %B %Y")

    # 🏫 LOGO (BIG + CENTERED)
    logo_path = "static/images/logo.png"
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=110, height=110)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 10))
        except:
            pass

    # 🏫 HEADER
    elements.append(Paragraph(f"{college.upper()}", title_style))
    elements.append(Paragraph(f"{class_info}", info_style))
    elements.append(Paragraph(f"Subject: {subject}", info_style))
    elements.append(Paragraph(f"Total Classes: {total_classes}", info_style))
    elements.append(Paragraph(f"Date: {date_str}", info_style))

    elements.append(Spacer(1, 20))

    # 📊 SUMMARY BOX
    avg = sum([s['percent'] for s in data]) / len(data)

    summary_table = Table([
        [Paragraph(f"Average Attendance: {avg:.1f}%", summary_style)]
    ], colWidths=[400])

    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#007BFF")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 0, colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 25))

    # 📋 TABLE DATA
    table_data = [["S.No", "Student Name", "Attended", "%", "Status"]]

    for i, s in enumerate(data, start=1):
        percent = s['percent']

        if percent >= 75:
            status = '<font color="green"><b>✔ Good</b></font>'
        else:
            status = '<font color="red"><b>✘ Low</b></font>'

        table_data.append([
            str(i),
            s['name'],
            str(s['attended']),
            f"{percent:.1f}%",
            Paragraph(status, styles['Normal'])
        ])

    table = Table(table_data, colWidths=[40, 180, 80, 60, 100])

    # 🎨 TABLE STYLE
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),

        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),

        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),

        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),

        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 40))

    # ✍️ SIGNATURE SECTION
    sign_table = Table([
        ["____________________", "____________________"],
        ["Teacher Signature", "HOD Signature"]
    ], colWidths=[250, 250])

    sign_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 20),
    ]))

    elements.append(sign_table)
    elements.append(Spacer(1, 20))

    # 📝 FOOTER
    elements.append(Paragraph(
        "This is a system-generated attendance report.",
        footer_style
    ))

    pdf.build(elements)

if __name__ == "__main__":
    app.run(debug=True)