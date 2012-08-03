# for some reason the first line is not shown on the poster
import mne

fname = 'raw.fif'
raw = mne.fiff.Raw(fname)
raw.info['bads'] = ['MEG 2443', 'EEG 053']  # mark bad channels

# filter data in beta band
raw.filter(13.0, 30.0, filter_length=4096, n_jobs=8)

# save filtered raw data
raw.save(fname[:-4] + '_beta.fif')

# extract epochs
picks = mne.fiff.pick_types(raw.info, meg=True, eeg=True, eog=True,
                            exclude=raw.info['bads'])
events = mne.find_events(raw, stim_channel='STI 014')
epochs = mne.Epochs(raw, events, event_id=1, tmin=-0.2, tmax=0.5, proj=True,
                    picks=picks, baseline=(None, 0), preload=True,
                    reject=dict(grad=4000e-13, mag=4e-12, eog=150e-6))

# compute evoked response and noise covariance
evoked = epochs.average()
cov = mne.compute_covariance(epochs, tmax=0)

# Plot evoked
mne.viz.plot_evoked(evoked)

# Inverse modeling

# compute inverse operator
fwd_fname = 'sample_audvis-meg-eeg-oct-6-fwd.fif'
fwd = mne.read_forward_solution(fwd_fname, surf_ori=True)
inv = mne.minimum_norm.make_inverse_operator(raw.info, fwd, cov, loose=0.2)

# compute inverse solution
stc = mne.minimum_norm.apply_inverse(evoked, inv, lambda2=1 / 3.0 ** 2,
                                     method='dSPM')

# morph it to average brain for group study
stc_avg = mne.morph_data('sample', 'fsaverage', stc, 5, smooth=5)
