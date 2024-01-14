# Install with `pip install mediawikiapi`
from mediawikiapi import MediaWikiAPI

mediawikiapi = MediaWikiAPI()

page = mediawikiapi.page("Energy efficiency in transport")

print(f"Page: {page.title}")
print(f"Summary: {page.summary[:100]}...")
print(f"{len(page.sections)} sections found - e.g.:")
for s in page.sections[:5]:
    print(f"{s}")
section_sel = page.sections[9]
print(f"Section text for {section_sel}: {page.section(section_sel)[:150]}...")

_ = input("\nPress any key to continue...")

print(page.content)
