daily_config = {
    'weight':
        {
            'tbl_name': 'weight',
            'date_name': 'Date',
            'y_axis': 'Weight',
            'y_lim_offset': 1, # number of month to get data from
            'y_lim_offset_percentage': 0
        },
    'weather_daily':
        {
            'tbl_name': 'weather_daily',
            'date_name': 'Date',
            'y_axis': 'Temp_mean',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        },
    'google_fit':
        {
            'tbl_name': 'google_fit',
            'date_name': 'Date',
            'y_axis': 'Step count',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        },
    'mood':
        {
            'tbl_name': 'mood',
            'date_name': 'Date',
            'y_axis': 'mood',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        }
}