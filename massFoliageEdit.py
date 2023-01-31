
""" 
    Editor Function to take the selected Procedural Foliage Spawner asset in Content Browser to batch apply settings 
    to all the foliage inside the spawner.

    Example to add new property:

    Go to here https://docs.unrealengine.com/4.27/en-US/PythonAPI/class/FoliageType_InstancedStaticMesh.html?highlight=foliagetype_instancedstaticmesh#unreal.FoliageType_InstancedStaticMesh
    and will show all editable properties or that type

    // Snippet from page
    Editor Properties: (see get_editor_property/set_editor_property)

            affect_distance_field_lighting (bool): [Read-Write] Controls whether the primitive should affect dynamic distance field lighting methods. This flag is only used if CastShadow is true.

            affect_dynamic_indirect_lighting (bool): [Read-Write] Controls whether the foliage should inject light into the Light Propagation Volume. This flag is only used if CastShadow is true.

            align_max_angle (float): [Read-Write] The maximum angle in degrees that foliage instances will be adjusted away from the vertical
    




    class AlignMaxAngle(FoliageProperty):                  <--------- Set new Class name
        def __init__(self,value):
            super().__init__(param_name="align_max_angle") <--------- Copy the property name
            self.value : float = value                     <--------- Set the variable type
    
    set_foliage_setting(AlignMaxAngle(5))                  <--------- Call the new setting in this function
"""

import unreal
import random


class FoliageProperty:
    """
        Link to doc to where all editable properties of FoliageType_InstancedStaticMesh are.
        https://docs.unrealengine.com/4.27/en-US/PythonAPI/class/FoliageType_InstancedStaticMesh.html?highlight=foliagetype_instancedstaticmesh#unreal.FoliageType_InstancedStaticMesh

        Base object for setting paramters on foliage instances
        Subclass and set "param_name" to the property of foliage type you would like to change. 
        I have included some common ones
    """
    def __init__(self,param_name):
        self.param = param_name
        self.value = None
        self.random_range : tuple(float,float) = None

    def set_params(self,instance):
        # Set the editor property with the param name and its value

        prop_value = self.value

        if self.random_range:
            prop_value = round(random.uniform(*self.random_range),2)     

        return instance.set_editor_property(self.param,prop_value)
    
    

class ProceduralScale(FoliageProperty):
    def __init__(self,min,max):
        super().__init__(param_name="procedural_scale")
        self.value = unreal.FloatInterval()
        self.value.min = min
        self.value.max = max

class MaxAge(FoliageProperty):
    def __init__(self,value):
        super().__init__(param_name="max_age")
        self.value : flaot = value

class SeedDensity(FoliageProperty):
    def __init__(self,value):
        super().__init__(param_name="initial_seed_density")
        self.value : float = value



def set_foliage_setting(setting=FoliageProperty, save=False):
    """
        Uses the selected Asset in the Contenet Browser, which should be of type "Procedural Foliage Spawner"
        Apply values to all folliage objects inside a foliage spawner
    
    Args:
        setting (FoliageProperty) An instance of FoliageProperty specifying the property to change

    """

    SelectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
    FoliageTypes = []

    # Get Selected Actors of Type ProceduralFoliageSpawner to get their foliage objects
    for asset in SelectedAssets:
        if type(asset)== unreal.ProceduralFoliageSpawner:
            for fol_type in asset.get_editor_property("foliage_types"):
                FoliageTypes.append(fol_type.get_editor_property('foliage_type_object'))

    for i in FoliageTypes:
        print(i)
        setting.set_params(i)
        if save:
            unreal.EditorAssetLibrary.save_loaded_asset(i)

if __name__ == "__main_":
    setting = SeedDensity(0.3)
    setting.random_range = (0.1,0.5)
    set_foliage_setting(setting)
