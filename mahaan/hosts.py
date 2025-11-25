from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'dash', 'dash.urls', name='dash'),  # Matches dash subdomain
    host(r'www', 'main.urls', name='main'),  # Matches dash subdomai
)
