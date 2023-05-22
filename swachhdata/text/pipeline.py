from tqdm.auto import tqdm

from .base import ModuleTextRecast

class Pipeline(ModuleTextRecast):

    def __init__(self, chain=[], verbose=1):
        
        super().__init__(verbose=verbose)
        self.id_pipeline = None
        self.chain = chain
    
    def __add__(self, other):
        if hasattr(self, 'id_pipeline') and hasattr(other, 'id_pipeline'):
            chain = self.chain + other.chain
        elif hasattr(self, 'id_pipeline') and not hasattr(other, 'id_pipeline'):
            chain = self.chain + [other]
        elif not hasattr(self, 'id_pipeline') and hasattr(other, 'id_pipeline'):
            chain = other.chain + [self]
        elif not hasattr(self, 'id_pipeline') and not hasattr(other, 'id_pipeline'):
            chain = [self] + [other]
        return Pipeline(chain)

    def __sub__(self, other):
        
        if hasattr(self, 'id_pipeline') and hasattr(other, 'id_base_recast'):
            if other in self.chain:
                self.chain.remove(other)
            else:
                raise ValueError(
                    f'{other} not found in Pipeline.chain'
                )
        return Pipeline(self.chain)

    def setup(self, text):
        super().setup(text)
    
    def recast(self):
        super().recast()

        recast_tqdm = tqdm(self.chain, leave=self._verbose_status, disable=self._verbose)
        for rec in recast_tqdm:
            recast_tqdm.set_postfix({f'Pipeline process': f'{rec._name}'})
            rec._verbose, rec._verbose_status = False, False
            self.data = rec.setup_recast(self.data)
        
        return self.data

    def setup_recast(self, text=None):
        self.setup(text)
        return self.recast()