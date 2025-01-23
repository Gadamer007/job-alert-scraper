import requests
import json
import os
import pandas as pd
from bs4 import BeautifulSoup

# List of job sources
job_sources = [
    "https://careers.msci.com/job-search",
    "https://www.ifrs.org/news-and-events/news/2024/05/join-the-staff-issb-technical-staff/",
    "https://jobsincarbon.niceboard.co/",
    "https://unjobs.org/duty_stations/ber/3",
    "https://www.ipcc.ch/about/vacancies/",
    "https://unjobs.org/offices/unep_bnn",
    "https://carbon-pulse.com/category/job-postings",
    "https://go2-markets.com/careers",
    "https://climatebase.org/jobs?q=carbon&scroll=true&location=Germany&l=ChIJAVkDPzdOqEcRcDteW0YgIQQ%3ABerlin%2C+Germany",
    "https://www.rootglobal.io/jobs",
    "https://www.globalreporting.org/about-gri/work-at-gri/",
    "https://climatechangejobs.com/jobs?q=carbon&location=Germany&location_id=168680",
    "https://www.klim.eco/",
    "https://careers.veyt.com/",
    "https://www.wwf.de/ueber-uns/stellenangebote",
    "https://www.cdrjobs.earth/job-board",
    "https://ecolytiq.com/company",
    "https://erm.wd3.myworkdayjobs.com/ERM_Careers?Region=4d7d7c99b7b10170bfb55b40c7278d13&locations=64e903afae3010015d111ff769d70000",
    "https://worldbankgroup.csod.com/ats/careersite/search.aspx?site=1&c=worldbankgroup&sid=%5e%5e%5eFLGscZMYY2RrwVaMR%2ftHYw%3d%3d",
    "https://jobs.careers.microsoft.com/global/en/search?lc=Berlin%2C%20Berlin%2C%20Germany&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true&ulcs=false&ref=cms",
    "https://jobs.eea.europa.eu/",
    "https://quantis.com/de/wer-wir-sind/talent/jobs-bei-quantis/",
    "https://sciencebasedtargets.org/about-us/join-our-team",
    "https://www.climatiq.io/about",
    "https://apply.workable.com/plana/#jobs",
    "https://n26.com/en-eu/careers",
    "https://jobs.eon.com/en?filter=locations.state%3ABerlin",
    "https://www.bmuv.de/ministerium/stellenausschreibungen",
    "https://www.climatepartner.com/en/career",
    "https://careers.blackrock.com/search-jobs/climate/45831/1",
    "https://jobs.giz.de/index.php?ac=search_result&search_criterion_country%5B%5D=46",
    "https://www.google.com/about/careers/applications/jobs/results?q=sustainability&has_remote=false&distance=50&hl=en_US&jlo=en_US",
    "https://perspectives.cc/careers/",
    "https://climate.jobs.personio.com/",
    "https://careers.southpole.com/locations/berlin",
    "https://hrms.iucn.org/iresy/index.cfm?event=vac.showOpenList",
    "https://www.ecologic.eu/jobs",
    "https://cdp-europe.jobs.personio.de/",
    "https://www.goldstandard.org/careers",
    "https://careers.nature.org/psc/tnccareers/APPLICANT/APPL/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_SCHJOB_FL&Action=U",
    "https://www.e3g.org/about/careers/",
    "https://careers.cozero.io/#jobs",
    "https://www.carbmee.com/career",
    "https://sjobs.brassring.com/TGnewUI/Search/Home/Home?partnerid=25965&siteid=5168#home",
    "https://sphera.com/",
    "https://pachama.com/careers/",
    "https://adelphi.de/en/career#job-offers",
    "https://de.indeed.com/",
    "https://www.impactpool.org/search?q=climate+change&countries%5B%5D=Germany&commit=search",
    "https://www.jobsingreen.eu/?language[]=en&locations.countryCode[]=DE&location.address=Berlin&locations.city[]=Berlin&query=%22climate%20change%22%20%22carbon%22&page=1",
    "https://anthesisgroup.pinpointhq.com/",
    "https://ecovadis.com/careers/",
    "https://winrock.org/work-with-us/careers/job-openings/",
    "https://dowjones.jobs/jobs/?location=Germany",
    "https://bezerocarbon.teamtailor.com/jobs/4823543-cdr-scientist-ratings?utm_content=305056273&utm_medium=social&utm_source=linkedin&hss_channel=lcp-54117489",
    "https://anewclimate.com/careers#block-views-blockjobs-block-job-posts",
    "https://greentrade.tech/careers/",
    "https://www.kuehne-stiftung.org/foundation/job-opportunities",
]

# Scraper function to search job listings within entire sites
def scrape_jobs():
    job_list = []
    for url in job_sources:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                job_url = link['href']
                if "job" in job_url.lower() or "careers" in job_url.lower():
                    if not job_url.startswith("http"):
                        job_url = url + job_url  # Ensure absolute URL
                    job_list.append({
                        "Job Title": link.text.strip() if link.text else "N/A",
                        "Organization": "Unknown",
                        "Summary": "N/A",
                        "Match %": "Unknown",
                        "Date Posted": "Unknown",
                        "Deadline": "Unknown",
                        "Job Type & Location": "Unknown",
                        "Link": job_url
                    })
        except requests.exceptions.RequestException as e:
            print(f"Network error scraping {url}: {e}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return job_list

# Send email via SendGrid
def send_email(job_list):
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    if not SENDGRID_API_KEY:
        print("SENDGRID_API_KEY is missing in environment variables.")
        return
    sender_email = "your-email@example.com"
    receiver_email = "dmlandholm@gmail.com"
    subject = "[Daily Job Alert] Climate & Carbon Roles"
    
    if not job_list:
        print("No job postings found. Skipping email.")
        return
    
    try:
        email_content = "<html><body><h2>Job Alerts</h2>" + pd.DataFrame(job_list).to_html(index=False) + "</body></html>"
    except Exception as e:
        print(f"Error generating email content: {e}")
        return

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [{"to": [{"email": receiver_email}]}],
        "from": {"email": sender_email},
        "subject": subject,
        "content": [{"type": "text/html", "value": email_content}]
    }
    
    try:
        response = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)
        response.raise_for_status()
        print("Email sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send email: {e}")

# Main execution
if __name__ == "__main__":
    job_data = scrape_jobs()
    send_email(job_data)





