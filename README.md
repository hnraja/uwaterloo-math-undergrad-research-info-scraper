# UWaterloo Math Undergrad Research Cold Email Generator

Web scraper to scrap information from https://uwaterloo.ca/statistics-and-actuarial-science/research/research-strengths into an Excel workbook for cold-email generation.

Let him cook
- Profiles that don't follow standard pattern, look for links called "Papers", "Publications", "Research" etc on personal pages
- Picking up some non-paper li elemets, regex to remove those "Authors (Year) Title Journal Volume/Page"
- Prof about me's
- Add links (Google scholar or uwlib with auth) to papers
- Fetch prof emails
- Add outlook uwaterloo auth to draft emails automatically based on template sheet
- Seeing some access denied, waterloo auth to access
- Cold email template sheet  à la *The Princess Bride*
  - Hello, my name is Inigo Montoya.
    - Name
    - Program
    - Year
  - You killed my father.
    - Took class?
    - Read paper?
  - Prepare to die.
    - Chat to discuss paper/research opportunities
    - Available at

Programming core is when you spend 5 hours building a web scraper when you could have done it faster manually. *C'est la vie*.