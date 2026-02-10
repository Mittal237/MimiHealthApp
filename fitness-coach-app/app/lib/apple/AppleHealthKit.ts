import { NativeModules } from "react-native";
import BrokenHealthKit from "react-native-health";

const AppleHealthKit: any = NativeModules.AppleHealthKit;

AppleHealthKit.Constants = (BrokenHealthKit as any).Constants;

export default AppleHealthKit;
