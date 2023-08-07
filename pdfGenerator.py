# importing libraries
from flask import Flask, render_template, make_response

# import pdfkit # https://pypi.org/project/pdfkit/ 
# issue for not using pdfkit is wkhtmltopdf. As we can't install wkhtmltopdf in the BTP
# https://stackoverflow.com/questions/73826411/how-to-install-and-run-wkhtmltopdf-on-ubuntu-22-04
import os
import weasyprint

# application initialization
app = Flask(__name__, template_folder="templates")

# fetching port details
cf_port = os.getenv("PORT")


@app.route("/API/GENERATE_PDF", methods=["GET"])
def generate_pdf():
    """Generate a PDF from a HTML Template"""
    # templateFile = "template.html"
    # Dummy data
    static_data = {
        "title": "Sample PDF Document created by Python",
        "name": "Kallol Chakraborty",
        "address": "Kolkata, WB",
    }
    # render the HTML template
    # renderTemplate = render_template(templateFile, data=userDetails)

    # with open("template.html", "r") as f:
    #     templateFile = f.read()

    # renderTemplate = render_template(templateFile, data=userDetails)
    # rendering HTML templates with the provided data
    renderTemplate = render_template("template.html", data=static_data)

    # generate PDF from the rendered HTML using WeasyPrint
    pdf = weasyprint.HTML(string=renderTemplate).write_pdf()

    # create the PDFKit object & pass the HTML into it
    # pdf = PDFkit(templateFile, output_file="Output.pdf")
    # pdfkit.from_string(renderTemplate, "Output.pdf")
    # return the PDF as response
    # response = make_response(open("Output.pdf", "r").read())
    # response.headers["Content-Type"] = "application/pdf"
    # response.headers["Content-Disposition"] = "attachment; filename=Output.pdf"

    # create a response using the PDF
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    # response = Response(pdf, content_type="application/pdf")
    response.headers["Content-Disposition"] = "inline; filename=Output.pdf"

    return response


if __name__ == "__main__":
    # If the app is running locally
    if cf_port is None:
        # Use port 5000
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        # Else use cloud foundry default port
        app.run(host="0.0.0.0", port=int(cf_port), debug=False)
