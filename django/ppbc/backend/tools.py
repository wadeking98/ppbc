import subprocess
class tools:
    def id_to_seed(id):
        """
        :param id the id number to be turned into a seed
        :type id int
        :return str the seed as a string
        """
        id_len = len(str(id))
        if id_len > 32:
            raise Exception("max users reached!")
        return "0"*(32-id_len)+str(id)
    
    def to_wallet(type, email):
        prefix = "o_" if type=="org" else "i_"
        return prefix+email.replace('@', '_').replace('.','_')


    def agent_running(wallet):
        wallet = wallet.strip("\n")
        ret = False
        proc = subprocess.Popen([
                "docker",
                "ps",
                "-f",
                "name="+wallet,
        ], stdout=subprocess.PIPE, encoding="utf-8")
        grep = subprocess.Popen([
            "grep",
            "-o",
            wallet
        ], stdin=proc.stdout, stdout=subprocess.PIPE, encoding="utf-8")
        try:
            out, err = grep.communicate(timeout=5)
            out = out.strip("\n")
            ret = (out==wallet)
            print((out, wallet))
        except:
            print("an unexpected error ocurred")
        finally:
            proc.kill()
            return ret

    


