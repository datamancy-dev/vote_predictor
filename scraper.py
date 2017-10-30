import vote_request as vr
import labeled_bill_request as lbr
import subprocess as sp

def run():
    """Runs things"""
    command_args=[(110, [2008])]

    
    #The longest computation time per iteration for loop I've ever written
    for carg in command_args:
        for year in carg[1]:
            vr.vote_request(carg[0], year, request_timer=2)
            lbr.lbl_list_request(carg[0], year, request_timer=2)
            upload_and_clean(carg[0], year)


def upload_and_clean(congress, year):
    gen_data = [vr.rp.get_bill_pickle_fp(congress, year, "h"),
                vr.rp.get_bill_pickle_fp(congress, year, "s"),
                vr.rp.get_vote_pickle_fp(congress, year, "h"),
                vr.rp.get_vote_pickle_fp(congress, year, "s"),
                vr.rp.get_bill_list(congress, year, "h"),
                vr.rp.get_bill_list(congress, year, "s")]

    for datum in gen_data:
        sp.call(["aws", "s3", "cp", "./" + datum, "s3://dsi-14-fern/"
                 + str(congress) + "-" + str(year) + "/"])
        sp.call(["rm", datum])
