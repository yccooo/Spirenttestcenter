# python version 3

from tkinter import Tcl
import os
import time


class TestCenter:
    def __init__(self, stc_install_dir):
        # create instance of Tcl object
        self.tclsh = Tcl()

        # check file exist
        filename = "SpirentTestCenter.tcl"
        filename = os.path.join(stc_install_dir, filename)

        if not os.path.exists(filename):
            print(f"not exist {filename}")
            return

        # load spirent testcent tcl API
        self.tclsh.eval("source {%s}" % filename)


    def create_porject(self,projectname):
        '''

        :param projectname: name of the project to create
        :return: createed project name
        '''
        print(f"Creating {projectname}...")

        cmd = f'''
        set {projectname} [stc::create project]
        '''
        self.tclsh.eval(cmd)

        print(f"Project {projectname} created")
        return projectname

    def create_port(self,portname,projectname,chassisip,slot):
        '''

        :param portname: name of the port to create
        :param projectname: project which the port belongs to
        :param chassisip: the chassis ip address of the port
        :param slot: the slot of the port
        :return: created port name
        '''

        location = f"//{chassisip}/{slot}"
        print(f"Creating the {portname}...")

        cmd = f'''        
        set {portname} [stc::create port -under ${{{projectname}}} -location {location}]
        '''
        self.tclsh.eval(cmd)

        print(f"Port {portname} created")
        return portname

    def create_streamblock(self,streamname,portname,
                           framelengthmode="FIXED",
                           fixframelength="128",
                           insertfcserror="FALSE",
                           insertsig="TRUE"):
        '''

        :param streamname: name of the stream to create
        :param portname: port which the stream belongs to
        :param framelengthmode: length mode of the stream
        :param fixframelength: specify the frame length when framelengthmode is FIXED
        :return: created stream name
        '''

        print(f"Creating/Configuring the {streamname} on the {portname}...")

        cmd = f'''        
        set {streamname} [stc::create "StreamBlock" \
        -under ${{{portname}}} \
        -FrameLengthMode {framelengthmode} \
        -FixedFrameLength {fixframelength} \
        -EnableFcsErrorInsertion {insertfcserror} \
        -InsertSig {insertsig} \
        -FrameConfig ""]
        '''
        self.tclsh.eval(cmd)

        print(f"Streamblock {streamname} creation completed")

        return streamname

    def create_ethernetII(self,streamblock,srcmac="00:10:94:00:12:34",dstmac="ff:ff:ff:ff:ff:ff",ethertype="88b5"):
        '''

        :param streamblock: the name of streamblock which want to add ethernetII header
        :param srcmac: source mac address
        :param dstmac: destination mac address
        :param ethertype: ethernet type
        :return: none
        '''

        print(f"Creating ethernetII on the {streamblock}")

        cmd = f'''
        stc::create ethernet:EthernetII -under ${{{streamblock}}} \
        -srcMac {srcmac} \
        -dstMac {dstmac} \
        -etherType {ethertype}
        '''
        self.tclsh.eval(cmd)

        print(f"Create ethernetII on the {streamblock} completed")

    def create_ipv4(self,streamblock,
                    srcip="192.85.1.2",
                    dstip="192.0.0.1",
                    destprefixlength="24",
                    protocol="253",
                    gateway="192.85.1.1"):
        '''

        :param streamblock: the name of streamblock which want to add ipv4 header
        :param srcip: source ip address
        :param dstip: destination ip address
        :param destprefixlength: prefix length of the destination ip address
        :param protocol: ip protocol
        :param gateway: the gateway to destination ip address
        :return: none
        '''

        print(f"Creating ipv4 on the {streamblock}")

        cmd = f'''
        stc::create ipv4:Ipv4 -under ${{{streamblock}}} \
        -sourceAddr {srcip} \
        -destAddr {dstip} \
        -destPrefixLength {destprefixlength} \
        -protocol {protocol} \
        -gateway {gateway}
        '''
        self.tclsh.eval(cmd)

        print(f"Create ipv4 on the {streamblock} completed")


    def create_ipv6(self,streamblock,
                    srcip="2000::2",
                    dstip="2000::1",
                    destprefixlength="64",
                    nextheader="59",
                    gateway="::0"):

        '''

        :param streamblock: the name of streamblock which want to add ipv6 header
        :param srcip: source ipv6 address
        :param dstip: destination ipv6 address
        :param destprefixlength: prefix length of the destination ipv6 address
        :param nextheader: next header protocol
        :param gateway: the gateway to destination ipv6 address
        :return: none
        '''

        print(f"Creating ipv6 on the {streamblock}")

        cmd = f'''
                stc::create ipv6:Ipv6 -under ${{{streamblock}}} \
                -sourceAddr {srcip} \
                -destAddr {dstip} \
                -destPrefixLength {destprefixlength} \
                -nextHeader {nextheader} \
                -gateway {gateway}
                '''
        self.tclsh.eval(cmd)

        print(f"Create ipv6 on the {streamblock} completed")




    def config_gengrator(self, portname,
                         durationmode="CONTINUOUS",
                         duration="10",
                         burstsize="1",
                         loadmode="FIXED",
                         loadunit="Percent",
                         fixedload="10"):
        '''

        :param portname: the name of the port which the gengerator belongs to
        :param durationmode: Length of transmission in terms of continuous, bursts, or seconds
        :param duration: Length of packet transmission. You specify the transmission unit by the duration mode
        :param loadmode: Load mode as fixed or random rate
        :patam fixedload: Fixed load value
        :return: none
        '''

        dict_1 = {
            "Percent": "PERCENT_LINE_RATE",
            "fps": "FRAMES_PER_SECOND",
            "bps": "BITS_PER_SECOND",
            "Kbps": "KILOBITS_PER_SECOND",
            "Mbps": "MEGABITS_PER_SECOND",
            "inter burst gap": "INTER_BURST_GAP",
            "L2 Rate": "L2_RATE"
        }

        loadunit_1 = loadunit.lower()

        loadunit = "PERCENT_LINE_RATE"

        if loadunit_1 == "percent":
            loadunit = dict_1["Percent"]
        if loadunit_1 == "fps":
            loadunit = dict_1["fps"]
        if loadunit_1 == "bps":
            loadunit = dict_1["bps"]
        if loadunit_1 == "kbps":
            loadunit = dict_1["Kbps"]
        if loadunit_1 == "mbps":
            loadunit = dict_1["Mbps"]
        if loadunit_1 == "inter burst gap":
            loadunit = dict_1["inter burst gap"]
        if loadunit_1 == "l2 rate":
            loadunit = dict_1["L2 Rate"]

        print(f"Configuring the generator on the {portname}...")

        cmd = f'''
        set generator_{portname} [stc::get ${{{portname}}} -children-Generator]
        
        set generatorconfig_{portname} [stc::get ${{generator_{portname}}} -children-GeneratorConfig]
        
        stc::config ${{generatorconfig_{portname}}} \
        -DurationMode {durationmode} \
        -Duration {duration} \
        -BurstSize {burstsize} \
        -LoadMode {loadmode} \
        -FixedLoad {fixedload} \
        -LoadUnit {loadunit}
        '''
        self.tclsh.eval(cmd)

        print(f"Generator of {portname} configuration completed")


    def config_analyzer(self,portname):
        '''

        :param portname: the name of the port which the analyzer belongs to
        :return: none
        '''

        print(f"Configuring the analyzer on the {portname}...")

        cmd = f'''
        set analyzer_{portname} [stc::get ${{{portname}}} -children-Analyzer]
        
        set analyzerconfig_{portname} [stc::get ${{analyzer_{portname}}} -children-AnalyzerConfig]
        
        stc::config ${{analyzerconfig_{portname}}} \
        -JumboFrameThreshold "1500" \
        -OversizeFrameThreshold "2000" \
        -UndersizeFrameThreshold "64" \
        -AdvSeqCheckerLateThreshold "1000" \
        '''
        self.tclsh.eval(cmd)

        print(f"Analyzer of {portname} configuration completed")


    def subscribe_result(self,projectname,object,configtype="Analyzer",resulttype="AnalyzerPortResults"):
        '''

        :param projectname: the project handle
        :param object: the object which statistics are to be collected
        :param configtype: the object type of the source object
        :param resulttype: the set of results
        :return: none
        '''

        print("Subscribing to results...")

        cmd = f'''
        set result [stc::subscribe -Parent ${{{projectname}}} \
        -ResultParent ${{{object}}} \
        -ConfigType {configtype} \
        -resulttype {resulttype}]
        '''
        self.tclsh.eval(cmd)

        print("Subscribe the result completed")


    def perform(self,object,*args):
        '''

        :param object: the command to perform
        :param args: args for command
        :return: none
        '''
        if args and len(args)==1:
            param = args[0]
        if args and len(args)>1:
            param = ','.join(args)

        if object.lower() == "attachports":
            if args:
                cmd = f'''
                puts "Performing AttachPorts"
                
                stc::perform AttachPorts -Portlist {param}
                
                puts "Attach ports completed"
                '''
            else:
                cmd = '''
                puts "Performing AttachPorts"
                
                stc::perform AttachPorts
                
                puts "Attach ports completed"
                '''

        if object.lower() == "chassisdisconnectall":
            if args:
                pass
            else:
                cmd = f'''
                puts "Performing ChassisDisconnectAll"

                stc::perform {object}

                puts "ChassisDisconnectAll completed"
                '''

        if object.lower() == "resetconfig":
            if args:
                pass
            else:
                cmd = f'''
                puts "Performing ResetConfig"

                stc::perform {object}

                puts "ResetConfig completed"
                '''

        self.tclsh.eval(cmd)


    def apply(self):

        print("Applying...")

        cmd ='''
        stc::apply
        '''
        self.tclsh.eval(cmd)

        print("Apply completed")


    def start(self,type,portname):
        '''

        :param type: analyzer or generator
        :param portname: the port to perform
        :return:
        '''

        if type.lower() == "analyzer":

            cmd = f'''
            puts "Starting analyzers on {portname}..."
            
            set analyzerCurrent [stc::get ${{{portname}}} -children-analyzer]
            stc::perform analyzerStart -analyzerList $analyzerCurrent
            
            puts "Analyzers started"
            '''

        if type.lower() == "generator":

            cmd = f'''
            puts "Starting traffic generation on {portname}..."

            set generatorCurrent [stc::get ${{{portname}}} -children-generator]
            stc::perform generatorStart -generatorList $generatorCurrent
            
            puts "Traffic generation started"
            '''

        self.tclsh.eval(cmd)

    def waituntilcompleted(self,timeout=0):
        '''

        :param timeout: the number of seconds the function will block before returning,regardless of the state of the sequencer
        :return: none
        '''
        print("Wait until command completed...")

        cmd = f'''
        stc::waitUntilComplete -timeout {timeout}
        '''

        self.tclsh.eval(cmd)
        print("Wait completed")


    def stop(self,type,portname):
        '''

        :param type: analyzer or generator
        :param portname: the port to perform
        :return: none
        '''

        if type.lower() == "analyzer":
            cmd = f'''
            puts "Stopping analyzers..."

            set analyzerCurrent [stc::get ${{{portname}}} -children-analyzer]
            stc::perform analyzerStop -analyzerList $analyzerCurrent

            puts "Analyzers stopped"
            '''

        if type.lower() == "generator":
            cmd = f'''
            puts "Stopping traffic generation..."

            set generatorCurrent [stc::get ${{{portname}}} -children-generator]
            stc::perform generatorStop -generatorList $generatorCurrent

            puts "Traffic generation stopped"
            '''

        self.tclsh.eval(cmd)


    def get_port_statistics(self,portname,type,attaribute):
        '''

        :param portname: the name of the port which to collected
        :param type: generator or analyzer
        :param attaribute: the attaribute to get. example: TotalFrameCount Ipv4FrameCount Ipv6FrameCount VlanFrameCount
        :return: collected statistics
        '''
        if type.lower() == "analyzer":
            cmd = f'''
            puts "Get individual stream block results";
            
            set analyzerCurrent [stc::get ${{{portname}}} -children-analyzer]
            set portResultsHnd [stc::get $analyzerCurrent -resultchild]
            set Fcount [stc::get $portResultsHnd -{attaribute}]
            '''
            self.tclsh.eval(cmd)

        return self.tclsh.getvar("Fcount")




stc_install_dir = r"D:\Program Files (x86)\Spirent Communications\Spirent TestCenter 5.35\Spirent TestCenter Application"
stc = TestCenter(stc_install_dir)

project1 = stc.create_porject("project1")

port1 = stc.create_port("port1",project1,"21.91.1.32","12/7")
port2 = stc.create_port("port2",project1,"21.91.1.32","12/8")

stc.perform("AttachPorts")

stream1 = stc.create_streamblock("stream1",port1)

stc.create_ethernetII(stream1,dstmac="3c:fd:fe:d5:ba:f2",ethertype="0800")

stc.create_ipv4(stream1,srcip="10.1.1.2",dstip="11.1.1.2",gateway="10.1.1.1")

stc.config_gengrator(port1,durationmode="bursts",duration="10")

stc.config_analyzer(port2)

stc.subscribe_result(project1,port2,"Analyzer","AnalyzerPortResults")

stc.apply()

stc.start("Analyzer",port2)

stc.start("Generator",port1)

time.sleep(3)

stc.stop("Generator",port1)

stc.stop("Analyzer",port2)

sta = stc.get_port_statistics(port2,"Analyzer","SigFrameCount")

print(sta)

stc.perform("ChassisDisconnectAll")

stc.perform("ResetConfig")






