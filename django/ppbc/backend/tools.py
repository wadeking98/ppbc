from .models import *
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

    def get_agent(request):
        return agent.objects.get(wallet_name=request.session["wallet"])

    def get_active_agent(request):
        agent_obj = tools.get_agent(request)
        return active_agent.objects.get(agent_id=agent_obj.id)

    


