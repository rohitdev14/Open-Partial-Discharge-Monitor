"""Simple deterministic pulse detector for Step 1B synthetic data."""
def detect_pulses(waveform, phase_deg, threshold=8.0, dead_time_samples=80):
    events=[]; i=0
    while i < len(waveform):
        if abs(waveform[i]) >= threshold:
            end=min(len(waveform),i+dead_time_samples)
            j=max(range(i,end),key=lambda k:abs(waveform[k]))
            events.append({"sample_index":j,"amplitude":round(waveform[j],6),
                           "phase_deg":round(phase_deg[j],3)})
            i=end
        else:
            i+=1
    return events
