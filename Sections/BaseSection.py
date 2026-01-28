from Sections.SectionBase import *

class BaseSection(SectionBase):
    """
    section defining space for all the base widgets (base decisions visible on startup)
    """
    def __init__(self, master, app):
        self.frame = FrameBase(master=master)

        self.accounting_bool = BooleanVar(value = False)
        self.payrolls_bool = BooleanVar(value = False)

        self.widgets = []

        self.checkboxes = (CheckBoxBase(master=self.frame,
                                        text="Mzdy",
                                        variable=self.payrolls_bool,
                                        command=lambda: app.toggle_relevant(self.payrolls_bool.get(),
                                                                            app.payrolls_section, 2)),
                           CheckBoxBase(master=self.frame,
                                        text="Účetnictví",
                                        variable=self.accounting_bool,
                                        command=lambda: app.toggle_relevant(self.accounting_bool.get(),
                                                                            app.accounting_section, 3)))

        self.setup_widgets()
        self.arrange_widgets(self.frame, self.widgets)

    def setup_widgets(self) -> None:
        """
        sets up widgets into default states with their default values
        :return: None
        """
        self.widgets.append(self.checkboxes)