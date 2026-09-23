"""PRPD feature builder for Step 1B."""
def build_prpd(events, phase_bin_deg=10):
    bins={}
    for event in events:
        phase=float(event["phase_deg"])%360.0
        key=int(phase//phase_bin_deg)*phase_bin_deg
        item=bins.setdefault(key,{"phase_start_deg":key,"count":0,"peak_abs_amplitude":0.0})
        item["count"]+=1
        item["peak_abs_amplitude"]=max(item["peak_abs_amplitude"],abs(float(event["amplitude"])))
    return [bins[k] for k in sorted(bins)]
