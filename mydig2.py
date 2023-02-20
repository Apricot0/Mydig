import datetime
import time
import dns.query

def mydig(domain_name,answers,cname):
    root_servers = ['198.41.0.4', '199.9.14.201', '192.33.4.12', '199.7.91.13', '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', '192.36.148.17', '192.58.128.30', '193.0.14.129', '199.7.83.42', '202.12.27.33']
    for root_server in root_servers:
        current_ser = root_server
        req = dns.message.make_query(domain_name, rdtype=dns.rdatatype.A)
        try:
            response = dns.query.udp(req, current_ser, timeout=5)
            break
        except dns.exception.Timeout:
            print("ERROR: connetion time out")
    print(f"{response}\n\n")
    for rrset in response.additional:
        for rr in rrset:
            if rr.rdtype == dns.rdatatype.A:
                dig(domain_name, answers, rr.address,cname) 
                return       
    return

def dig(domain_name, answers, source, cname):
    req = dns.message.make_query(domain_name, rdtype=dns.rdatatype.A)
    try:
        response = dns.query.udp(req, source, timeout=5)
        print (f"{response}\n\n")
    except dns.exception.Timeout:
        print("ERROR: connetion time out")
    if response.answer:
        for rrset in response.answer:
            ttl = rrset.ttl
            print (ttl)
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.CNAME:
                    cname.append(str(rr.target))
                    mydig(rr.target, answers, cname)
                    return
                elif rr.rdtype == dns.rdatatype.A:
                    answers.append(rr.address)
        return
    if response.additional:
        for rrset in response.additional:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.A:
                    dig(domain_name, answers, rr.address, cname)
                    return  
        return                     
    if response.authority:
        re = []
        cn = []
        for rrset in response.authority:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.NS:
                    mydig(rr.target.to_text(), re, cn)
                    for x in re:
                        dig(domain_name, answers, x, cname)
                    return
        return            
    return


if __name__ == '__main__':
    answers = []
    cnames = []
    #dom = input("Enter a domain name: ")
    start_time = time.time()
    mydig("www.bbc.com",answers,cnames)
    end_time = time.time()
    print("QUESTION SECTION:")
    #print(f"{dom}\t\tIN A")
    print(f"ANSWER SECTION:\n{set(answers)}\n{set(cnames)}")  