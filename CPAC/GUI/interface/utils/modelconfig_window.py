import wx
import generic_class
from .constants import control, dtype, substitution_map
import os
import ast
import yaml


ID_RUN = 11


class ModelConfig(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(
            self, parent=parent, title="CPAC - Create New FSL Model", size=(900, 590))

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.panel = wx.Panel(self)

        self.window = wx.ScrolledWindow(self.panel)

        self.page = generic_class.GenericClass(self.window, "FSL Model Setup")

        self.page.add(label="Subject List ",
                      control=control.COMBO_BOX,
                      name="subjectListFile",
                      type=dtype.STR,
                      comment="Full path to a list of subjects to be included in the model.\n\nThis should be a text file with one subject per line.\n\nTip 1: A list in this format contaning all subjects run through CPAC was generated along with the main CPAC subject list (see subject_list_group_analysis.txt).\n\nTIp 2: An easy way to manually create this file is to copy the subjects column from your Regressor/EV spreadsheet.",
                      values="")

        self.page.add(label="EV File ",
                      control=control.COMBO_BOX,
                      name="phenotypicFile",
                      type=dtype.STR,
                      comment="Full path to a .csv file containing EV information for each subject.\n\nTip: A file in this format (containing a single column listing all subjects run through CPAC) was generated along with the main CPAC subject list (see template_phenotypic.csv).",
                      values="")

        self.page.add(label="Subjects Column Name ",
                      control=control.TEXT_BOX,
                      name="subjectColumn",
                      type=dtype.STR,
                      comment="Name of the subjects column in your EV file.",
                      values="",
                      style=wx.EXPAND | wx.ALL,
                      size=(160, -1))

        self.page.add(label="EVs to Include ",
                      control=control.TEXT_BOX,
                      name="columnsInModel",
                      type=dtype.LSTR,
                      comment="Specify the names of columns in your EV file that you would like to include in this model.\n\nColumn names should be separated by commas and appear exactly as they do in your EV file.",
                      values="",
                      style=wx.EXPAND | wx.ALL,
                      size=(600, -1))

        self.page.add(label="EV Type ",
                      control=control.TEXT_BOX,
                      name="categoricalVsDirectional",
                      type=dtype.LNUM,
                      comment="Specify whether each of the EVs in this model should be treated as categorical or continuous.\n\nTo do this, place a 1 (categorical) or 0 (continuous) in the same list position as the corresponding EV.\n\nFor example, if the EVs to include were:\nage, sex, diagnosis, mean_fd\n\nOne might specify:\n0,1,1,0",
                      values="",
                      style=wx.EXPAND | wx.ALL,
                      size=(160, -1))

        self.page.add(label="Demean ",
                      control=control.TEXT_BOX,
                      name="deMean",
                      type=dtype.LNUM,
                      comment="Specify whether to demean each of the EVs in this model.\n\nTo do this, place a 1 (demean) or 0 (don't demean) in the same list position as the corresponding EV.\n\nFor example, if the EVs to include were:\nage, sex, diagnosis, mean_fd\n\nOne might specify:\n1,0,0,1\n\nNote that only continuous EV's should be demeaned.",
                      values="",
                      style=wx.EXPAND | wx.ALL,
                      size=(160, -1))

        self.page.add(label="Contrast File ",
                      control=control.COMBO_BOX,
                      name="contrastFile",
                      type=dtype.STR,
                      comment="Full path to a .csv file containing contrasts to be applied to this model.\n\nWhen specifying EVs in this file:\n\n- Continuous EVs should appear the same as their corresponding column name in the EV file.\n\n- Categorical EVs must be split into multiple columns (one for each category), with names of the format EVname__N (e.g. diagnosis__1, diagnosis__2, diagnosis__3)\n\nIf you wish to include F-tests in your model, create a column for each desired F-test, with names in the format f_test_1, f_test_2, etc.",
                      values="")


        self.page.add(label="Model Group Variances Seperately ",
                      control=control.CHOICE_BOX,
                      name='modelGroupVariancesSeparately',
                      type=dtype.NUM,
                      comment="Specify whether FSL should model the variance for each group separately.\n\nIf this option is enabled, you must specify a grouping variable below.",
                      values=["Off", "On"])

        self.page.add(label="Grouping Variable ",
                      control=control.TEXT_BOX,
                      name="groupingVariable",
                      type=dtype.STR,
                      comment="The name of the EV that should be used to group subjects when modeling variances.\n\nIf you do not wish to model group variances separately, set this value to None.",
                      values="None",
                      size=(160, -1))

        self.page.add(label="Model Name ",
                      control=control.TEXT_BOX,
                      name="modelName",
                      type=dtype.STR,
                      comment="Specify a name for the new model.",
                      values="",
                      size=(200, -1))

        self.page.add(label="Output Directory ",
                      control=control.DIR_COMBO_BOX,
                      name="outputModelFilesDirectory",
                      type=dtype.STR,
                      comment="Full path to the directory where CPAC should place model files.",
                      values="")

        self.page.add(label="Model CSV File Name ",
                      control=control.TEXT_BOX,
                      name="outputModelFile",
                      type=dtype.STR,
                      comment="In addition to the standard FSL model files, CPAC will output a .csv containing the subjects and EVs specified above.\n\nColumn names in this file will be the same as in the contrasts file, and will have been demeaned as specified.",
                      values="",
                      style=wx.EXPAND | wx.ALL,
                      size=(600, -1),
                      validation_req = False)

        self.page.set_sizer()

        mainSizer.Add(self.window, 1, wx.EXPAND)

        btnPanel = wx.Panel(self.panel, -1)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        run = wx.Button(btnPanel, ID_RUN, "Create Model", (
            280, -1), wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, lambda event: self.save(
            event, 'run'), id=ID_RUN)
        hbox.Add(run, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=10)

        buffer = wx.StaticText(btnPanel, label="\t\t\t\t\t\t")
        hbox.Add(buffer)

        cancel = wx.Button(btnPanel, wx.ID_CANCEL, "Cancel", (
            220, 10), wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.cancel, id=wx.ID_CANCEL)
        hbox.Add(cancel, 0, flag=wx.LEFT | wx.BOTTOM, border=5)

        load = wx.Button(btnPanel, wx.ID_ADD, "Load Settings", (
            200, -1), wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.load, id=wx.ID_ADD)
        hbox.Add(load, 0.6, flag=wx.LEFT | wx.BOTTOM, border=5)

        save = wx.Button(btnPanel, wx.ID_SAVE, "Save Settings", (
            200, -1), wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, lambda event: self.save(
            event, 'save'), id=wx.ID_SAVE)
        hbox.Add(save, 0.6, flag=wx.LEFT | wx.BOTTOM, border=5)

        btnPanel.SetSizer(hbox)

        mainSizer.Add(
            btnPanel, 0.5,  flag=wx.ALIGN_RIGHT | wx.RIGHT, border=20)

        self.panel.SetSizer(mainSizer)

        self.Show()

    def cancel(self, event):
        self.Close()

    def display(self, win, msg):
        wx.MessageBox(msg, "Error")
        win.SetBackgroundColour("pink")
        win.SetFocus()
        win.Refresh()
        raise ValueError

    def validate(self, config_map):
        try:
            import ast

            columns = [v.strip()
                       for v in config_map.get('columnsInModel')[1].split(",")]

            if not columns:
                self.display(config_map.get('columnsInModel')[
                             0], "No columns specified for the model")
                return -1

            for key, val in config_map.iteritems():

                if key != 'groupingVariable' and len(val[1]) == 0:
                    self.display(val[0], "%s field is empty!" % key)

                if '/' in val[1] and val[2]:
                    if not os.path.exists(val[1]):
                        self.display(val[
                                     0], "%s field contains incorrect path. Please enter correct path!" % key)

                if key == 'categoricalVsDirectional' or key == 'deMean':
                    value = [int(v) for v in val[1].split(",")]
                    for v in value:
                        if v not in [1, 0]:
                            self.display(val[
                                         0], "Invalid Entry. Only 1 and 0 entry allowed")

                    if len(value) != len(columns):
                        self.display(val[
                                     0], "Number of values in %s do not match specified columns in the model" % key)

                if key == 'groupingVariable':
                    if str(config_map.get('modelGroupVariancesSeparately')[1]) == "On":
                        if len(val[1]) == 0:
                            self.display(val[0], "%s field is empty!" % key)

                        if val[1] not in columns:
                            self.display(val[
                                         0], "Grouping variable/column not a valid column in the model. Please verify the name")

            return 1

        except Exception:
            return -1

    def run_model(self, config):
        try:
            print "executing fsl model"
            import CPAC
            CPAC.utils.create_fsl_model.run(config)
            return 1
        except ImportError, e:
            wx.MessageBox(
                "Error importing CPAC. Unable to run FSL Create Model tool.", "Error")
            print "Error importing CPAC"
            print e
            return -1
        except Exception, e:
            wx.MessageBox("Error running fsl create model. %s" % e, "Error")
            print "Error running fsl create model tool. Problem with the configuration"
            print e
            return -1

    def save(self, event, flag):

        config_list = []
        config_map = {}

        for ctrl in self.page.get_ctrl_list():

            print "validating ctrl-->", ctrl.get_name()
            print "ctrl.get_selection()", ctrl.get_selection()
            print "type(ctrl.get_selection())", type(ctrl.get_selection())

            win = ctrl.get_ctrl()
            value = str(ctrl.get_selection())
            name = ctrl.get_name()
            dtype = ctrl.get_datatype()
            validation = ctrl.get_validation()
            help = ctrl.get_help()

            config_list.append((name, value, dtype, help))
            config_map[name] = [win, value, validation]

        try:
            if self.validate(config_map) > 0:
                dlg = wx.FileDialog(self, message="Save file as ...",
                                    defaultDir=os.getcwd(),
                                    defaultFile="config_fsl.yaml",
                                    wildcard="YAML files(*.yaml, *.yml)|*.yaml;*.yml",
                                    style=wx.SAVE)

                if dlg.ShowModal() == wx.ID_OK:

                    path = dlg.GetPath()
                    f = open(path, 'w')
                    dlg.Destroy()
                    for item in config_list:
                        if item[2] == 2:
                            value = substitution_map.get(str(item[1]))
                            if value is None:
                                value = ast.literal_eval(item[1])
                        elif item[2] == 5:
                            value = [v for v in ast.literal_eval(item[1])]
                        elif item[2] == 4:
                            value = [str(v.strip())
                                     for v in item[1].split(',')]
                        else:
                            value = str(item[1])

                        for lines in item[3].split('\n'):
                            print >> f, "#", lines

                        print >> f, item[0], ": ", value, "\n"

                    print "saving %s" % path
                    f.close()

                    if flag == 'run':
                        if self.run_model(path) > 0:
                            self.Parent.box1.GetTextCtrl().SetValue(
                                config_map.get('outputModelFilesDirectory')[1])
                            self.Parent.box2.GetTextCtrl().SetValue(
                                config_map.get('subjectListFile')[1])
                            self.Close()

        except Exception:
            print "error writing temp file "
            raise

    def load(self, event):

        dlg = wx.FileDialog(
            self, message="Choose the config fsl yaml file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="YAML files(*.yaml, *.yml)|*.yaml;*.yml",
            style=wx.OPEN | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            config_map = yaml.load(open(path, 'r'))
            s_map = dict((v, k) for k, v in substitution_map.iteritems())

            for ctrl in self.page.get_ctrl_list():
                name = ctrl.get_name()
                value = config_map.get(name)
                dtype = ctrl.get_datatype()
                if isinstance(value, list):
                    val = None
                    for v in value:
                        if val:
                            val = val + "," + str(v)
                        else:
                            val = str(v)
                else:
                    val = s_map.get(value)
                    if val == None:
                        val = value

                # print "setting value in ctrl name, value -->", name, val
                ctrl.set_value(str(val))

            dlg.Destroy()
