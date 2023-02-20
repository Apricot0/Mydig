import dns.resolver

# Set the domain name you want to resolve
domain_name = 'www.cnn.com'

# Set the initial resolver to use
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']  # Use Google's public DNS server

# Send a query for the domain name to the resolver
query = dns.message.make_query(domain_name, dns.rdatatype.A)
response = dns.query.udp(domain_name, 'A')

# Check if the response contains an answer or the authoritative name server
while not response.answer and response.authority:
    ns_rrset = response.authority[0]  # Get the first RRset in the authority section
    ns = ns_rrset[0].target  # Get the target name for the NS record
    query = dns.message.make_query(domain_name, dns.rdatatype.A)
    response = dns.query.udp(query, str(ns))

if response.answer:
    print(response.answer)
else:
    print("No answer found for domain name")