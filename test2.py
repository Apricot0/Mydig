import datetime
import time
import dns.query

def mydig(domain_name,answers):
    root_servers = ['198.41.0.4', '199.9.14.201', '192.33.4.12', '199.7.91.13', '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', '192.36.148.17', '192.58.128.30', '193.0.14.129', '199.7.83.42', '202.12.27.33']
    start_time = time.time()
    result = None
    for root_server in root_servers:
        current_ser = root_server
        req = dns.message.make_query(domain_name, rdtype=dns.rdatatype.A)
        try:
            response = dns.query.udp(req, current_ser, timeout=5)
            break
        except dns.exception.Timeout:
            print("time out")
    while True:            
        print(f"{response}\n\n")
        if response.answer:
            answers.append(response.answer)
            for rrset in response.answer:
                for rr in rrset:
                    if rr.rdtype == dns.rdatatype.CNAME:
                        print(rr.target)
                        mydig(rr.target, answers)
            return            
        if response.additional:
            for rrset in response.additional:
                for rr in rrset:
                    if rr.rdtype == dns.rdatatype.A:
                        current_ser=rr.adress          

def dig(domain_name, answers, source):
    req = dns.message.make_query(domain_name, rdtype=dns.rdatatype.A)
    try:
        response = dns.query.udp(req, source, timeout=5)
        #print (f"{response}\n\n")
    except dns.exception.Timeout:
        print("time out")
    if response.answer:
        answers.append(response.answer)
        for rrset in response.answer:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.CNAME:
                    print(rr.target)
                    mydig(rr.target, answers)
        return
    if response.additional:
        for rrset in response.additional:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.A:
                    dig(domain_name, answers, rr.address)
    
    if response.authority:
        for rrset in response.additional:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.NS:
                    dig(domain_name, answers, rr.address)


if __name__ == '__main__':
    #domain_name = input("Enter a domain name: ")
    answers = []
    mydig("www.google.com",answers)
    print(f"ANNS:\n{set(answers)}")                     