import datetime
import dns.query

def mydig(domain_name,answers,cname,onlyAd):
    root_servers = ['198.41.0.4', '199.9.14.201', '192.33.4.12', '199.7.91.13', '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', '192.36.148.17', '192.58.128.30', '193.0.14.129', '199.7.83.42', '202.12.27.33']
    for root_server in root_servers:
        current_ser = root_server
        req = dns.message.make_query(domain_name, rdtype=dns.rdatatype.A)
        try:
            response = dns.query.udp(req, current_ser, timeout=5)
            break
        except dns.exception.Timeout:
            print("ERROR: connetion time out")
    for rrset in response.additional:
        for rr in rrset:
            if rr.rdtype == dns.rdatatype.A:
                dig(domain_name, answers, rr.address,cname, onlyAd) 
                return       
    return

def dig(domain_name, answers, source, cname, onlyAd):
    req = dns.message.make_query(domain_name, rdtype=dns.rdatatype.A)
    try:
        response = dns.query.udp(req, source, timeout=5)
    except dns.exception.Timeout:
        print("ERROR: connetion time out")
    if response.answer:
        for rrset in response.answer:
            ttl = rrset.ttl
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.CNAME:
                    cname.append(str(f"{domain_name}\t\t{ttl}\tIN\tCNAME\t{rr.target}"))
                    mydig(rr.target, answers, cname, onlyAd)
                    return
                elif rr.rdtype == dns.rdatatype.A:
                    answers.append(str(f"{domain_name}\t{ttl}\tIN\tA\t{rr.address}"))
                    onlyAd.append(rr.address)
        return
    if response.additional:
        for rrset in response.additional:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.A:
                    dig(domain_name, answers, rr.address, cname, onlyAd)
                    return  
        return                     
    if response.authority:
        re = []
        cn = []
        da = []
        for rrset in response.authority:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.NS:
                    mydig(rr.target.to_text(), re, cn, da)
                    for x in da:
                        dig(domain_name, answers, x, cname, onlyAd)
                    return
        return            
    return


if __name__ == '__main__':
    answers = []
    cnames = []
    onlyAd =[]
    dom = input("Enter a domain name: ")
    start_time = datetime.datetime.now()
    mydig(dom,answers,cnames,onlyAd)
    end_time = datetime.datetime.now()
    query_time = (end_time - start_time).total_seconds() * 1000
    print("QUESTION SECTION:")
    print(f"{dom}\t\t\tIN\tA")
    print()
    print("ANSWER SECTION:")
    for x in cnames:
        print(x)
    for y in answers:
        print(y)
    print()
    print(f'Query time: {query_time:.3f} msec')
    print(f'WHEN: {start_time.strftime("%a %b %d %H:%M:%S %Y")}')