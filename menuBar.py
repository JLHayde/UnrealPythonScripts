import unreal

class UEMenuBar:
    def __init__(self, menu_name="Custom Shelf", replace=True):

        self.menu_name = menu_name
        self._menus = unreal.ToolMenus.get()
        self.UEMainWindowBar = self._menus.find_menu('MainFrame.MainMenu')

        self.menu_items = {}
        self.sections = {}
        self.tool_shelf = self.UEMainWindowBar.add_sub_menu(self.UEMainWindowBar.get_name(), self.menu_name, self.menu_name, self.menu_name)
    
    def _menu_name(self,name):
        return "Custom.{}.{}".format(self.menu_name,name)
    
    def _shelf_name(self,name):
        return "shelf.{}".format(name)

    
    def add_menu_item(self,label,function,section="Tools"):

        # Create Section header if none exsist
        if not self.sections.get("shelf.{}".format(section)):
            self.sections["shelf.{}".format(section)] = self.tool_shelf.add_section("shelf.{}".format(section),
                                                                                            section,
                                                                                            section,
                                                                                            unreal.ToolMenuInsertType.DEFAULT)

        # Construct the Menu Item Entry
        self.menu_items[label] = unreal.ToolMenuEntry(name="Custom.{}.{}".format(self.menu_name,label),
                                                                type=unreal.MultiBlockType.MENU_ENTRY,
                                                                insert_position=unreal.ToolMenuInsert("",
                                                                unreal.ToolMenuInsertType.DEFAULT))
        # Set Item Functions and label
        self.menu_items[label].set_label(label)
        self.menu_items[label].set_string_command(unreal.ToolMenuStringCommandType.PYTHON,unreal.Name("Name"), string=(function))
        # Add the item to the shelf
        self.tool_shelf.add_menu_entry("shelf.{}".format(section,label), self.menu_items[label])


tools = {"Print Foo": "print('foo')",
        "Print Bar": "print('bar')"}

MyMenu = UEMenuBar()

for name,action in tools.items():
    MyMenu.add_menu_item(name,action, section="Print Section")
