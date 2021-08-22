from dateutil import tz, parser

from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestToBase(TransactionCase):

    def setUp(self):
        super(TestToBase, self).setUp()

    # TC01
    def test_barcode_exists(self):
        test_values = [{'name': f'{x}00' * 3} for x in range(10)]
        self.env['res.partner'].create(test_values)

        self.assertTrue(
            self.env['to.base'].barcode_exists(
                barcode='000000000',
                model_name='res.partner',
                barcode_field='name',
                inactive_rec=False,
            ),
            "\nTest case TC01",
        )

    # TC02
    def test_get_ean13(self):
        # Test with valid values
        test_vals = [
            '123123123123',
            '978020137962',
            '978053237962',
            '978053225412',
            '1234',
            '0',
        ]

        check_vals = [
            '1231231231232',
            '9780201379624',
            '9780532379621',
            '9780532254126',
            '0000000012348',
            '0000000000000',
        ]

        for i in range(len(test_vals)):
            self.assertEqual(
                check_vals[i],
                self.env['to.base'].get_ean13(test_vals[i]),
                'Test case TC02',
            )

        # Test with invalid values
        with self.assertRaises(ValueError):
            self.env['to.base'].get_ean13('abcdef')

    # TC03
    def test_convert_time_to_utc(self):
        test_dt = parser.isoparse('2020-02-02 18:32:11.00')
        converted_dt = self.env['to.base'].convert_time_to_utc(
            dt=test_dt, tz_name='Asia/Ho_Chi_Minh'
        )

        check_dt = parser.isoparse('2020-02-02 11:32:11.00')
        check_dt = check_dt.replace(tzinfo=tz.UTC)

        self.assertEqual(check_dt, converted_dt, 'Test case TC03')

    # TC04
    def test_convert_utc_time_to_tz(self):
        test_dt = parser.isoparse('2020-02-02 11:42:23.00')
        converted_dt = self.env['to.base'].convert_utc_time_to_tz(
            utc_dt=test_dt, tz_name='Asia/Ho_Chi_Minh'
        )

        check_dt = parser.isoparse('2020-02-02 18:42:23.00')
        check_dt = check_dt.replace(tzinfo=tz.gettz('Asia/Ho_Chi_Minh'))

        self.assertEqual(check_dt, converted_dt, 'Test case TC04')

    # TC05
    def test_time_to_float_hour(self):
        test_vals = [parser.isoparse('2021-01-01 19:50:25.230')]
        check_vals = [19.840341666666664]
        for i in range(len(test_vals)):
            self.assertEqual(
                check_vals[i],
                self.env['to.base'].time_to_float_hour(dt=test_vals[i]),
                "\nTest case TC05",
            )

    # TC06
    def test_find_first_date_of_period(self):
        # Test weekly
        test_weekly = [
            parser.isoparse('2021-03-04 18:00:00.00'),
            parser.isoparse('2021-03-01 00:00:00.00'),
            parser.isoparse('2021-03-07 23:59:59.00'),
        ]
        check_weekly = [
            parser.isoparse('2021-03-01 18:00:00.00'),
            parser.isoparse('2021-03-01 00:00:00.00'),
            parser.isoparse('2021-03-01 23:59:59.00'),
        ]
        for i in range(len(test_weekly)):
            self.assertEqual(
                check_weekly[i],
                self.env['to.base'].find_first_date_of_period(
                    period_name='weekly', date=test_weekly[i]
                ),
                "\nTest case TC06.01 - Test weekly",
            )

        # Test monthly
        test_monthly = [
            parser.isoparse('2021-03-12 19:53:11.00'),
            parser.isoparse('2021-03-01 00:00:00.00'),
            parser.isoparse('2021-03-31 23:59:59.00'),
        ]
        check_monthly = [
            parser.isoparse('2021-03-01 19:53:11.00'),
            parser.isoparse('2021-03-01 00:00:00.00'),
            parser.isoparse('2021-03-01 23:59:59.00'),
        ]
        for i in range(len(test_monthly)):
            self.assertEqual(
                check_monthly[i],
                self.env['to.base'].find_first_date_of_period(
                    period_name='monthly', date=test_monthly[i]
                ),
                "\nTest case TC06.02 - Test monthly",
            )

        # Test quarterly
        test_quarterly = [
            parser.isoparse('2021-03-04 18:03:24.00'),
            parser.isoparse('2021-05-01 00:01:01.00'),
            parser.isoparse('2021-09-25 19:50:11.00'),
            parser.isoparse('2021-11-12 14:20:11.00'),
            parser.isoparse('2021-01-01 00:00:00.00'),
            parser.isoparse('2021-03-31 23:59:59.00'),
            parser.isoparse('2021-04-01 00:00:00.00'),
            parser.isoparse('2021-06-30 23:59:59.00'),
            parser.isoparse('2021-07-01 00:00:00.00'),
            parser.isoparse('2021-09-30 23:59:59.00'),
            parser.isoparse('2021-10-01 00:00:00.00'),
            parser.isoparse('2021-12-31 23:59:59.00'),
        ]
        check_quarterly = [
            parser.isoparse('2021-01-01 18:03:24.00'),
            parser.isoparse('2021-04-01 00:01:01.00'),
            parser.isoparse('2021-07-01 19:50:11.00'),
            parser.isoparse('2021-10-01 14:20:11.00'),
            parser.isoparse('2021-01-01 00:00:00.00'),
            parser.isoparse('2021-01-01 23:59:59.00'),
            parser.isoparse('2021-04-01 00:00:00.00'),
            parser.isoparse('2021-04-01 23:59:59.00'),
            parser.isoparse('2021-07-01 00:00:00.00'),
            parser.isoparse('2021-07-01 23:59:59.00'),
            parser.isoparse('2021-10-01 00:00:00.00'),
            parser.isoparse('2021-10-01 23:59:59.00'),
        ]
        for i in range(len(test_quarterly)):
            self.assertEqual(
                check_quarterly[i],
                self.env['to.base'].find_first_date_of_period(
                    period_name='quarterly', date=test_quarterly[i]
                ),
                "\nTest case TC06.03 - Test quarterly",
            )

        # Test biannually
        test_biannually = [
            parser.isoparse('2021-03-04 18:00:00.00'),
            parser.isoparse('2021-10-25 08:01:00.00'),
            parser.isoparse('2021-01-01 00:00:00.00'),
            parser.isoparse('2021-06-30 23:59:59.00'),
            parser.isoparse('2021-07-01 00:00:00.00'),
            parser.isoparse('2021-12-31 23:59:59.00'),
        ]
        check_biannually = [
            parser.isoparse('2021-01-01 18:00:00.00'),
            parser.isoparse('2021-07-01 08:01:00.00'),
            parser.isoparse('2021-01-01 00:00:00.00'),
            parser.isoparse('2021-01-01 23:59:59.00'),
            parser.isoparse('2021-07-01 00:00:00.00'),
            parser.isoparse('2021-07-01 23:59:59.00'),
        ]
        for i in range(len(test_monthly)):
            self.assertEqual(
                check_biannually[i],
                self.env['to.base'].find_first_date_of_period(
                    period_name='biannually', date=test_biannually[i]
                ),
                "\nTest case TC06.04 - Test biannually",
            )

    # TC07
    def test_find_last_date_of_period(self):
        # Test weekly
        test_weekly = [
            parser.isoparse('2021-03-04 18:11:23.00'),
            parser.isoparse('2021-03-01 00:00:00.00'),
            parser.isoparse('2021-03-07 23:59:59.00'),
        ]
        check_weekly = [
            parser.isoparse('2021-03-07 18:11:23.00'),
            parser.isoparse('2021-03-07 00:00:00.00'),
            parser.isoparse('2021-03-07 23:59:59.00'),
        ]
        for i in range(len(test_weekly)):
            self.assertEqual(
                check_weekly[i],
                self.env['to.base'].find_last_date_of_period(
                    period_name='weekly', date=test_weekly[i]
                ),
                "\nTest case TC07.01 - Test weekly",
            )

        # Test monthly
        test_monthly = [
            parser.isoparse('2021-03-12 19:53:11.00'),
            parser.isoparse('2021-03-01 00:00:00.00'),
            parser.isoparse('2021-03-31 23:59:59.00'),
        ]
        check_monthly = [
            parser.isoparse('2021-03-31 19:53:11.00'),
            parser.isoparse('2021-03-31 00:00:00.00'),
            parser.isoparse('2021-03-31 23:59:59.00'),
        ]
        for i in range(len(test_monthly)):
            self.assertEqual(
                check_monthly[i],
                self.env['to.base'].find_last_date_of_period(
                    period_name='monthly', date=test_monthly[i]
                ),
                "\nTest case TC07.02 - Test monthly",
            )

        # Test quarterly
        test_quarterly = [
            parser.isoparse('2021-03-04 18:03:24.00'),
            parser.isoparse('2021-05-01 00:01:01.00'),
            parser.isoparse('2021-09-25 19:50:11.00'),
            parser.isoparse('2021-11-12 14:20:11.00'),
            parser.isoparse('2021-01-01 00:00:00.00'),
            parser.isoparse('2021-03-31 23:59:59.00'),
            parser.isoparse('2021-04-01 00:00:00.00'),
            parser.isoparse('2021-06-30 23:59:59.00'),
            parser.isoparse('2021-07-01 00:00:00.00'),
            parser.isoparse('2021-09-30 23:59:59.00'),
            parser.isoparse('2021-10-01 00:00:00.00'),
            parser.isoparse('2021-12-31 23:59:59.00'),
        ]
        check_quarterly = [
            parser.isoparse('2021-03-31 18:03:24.00'),
            parser.isoparse('2021-06-30 00:01:01.00'),
            parser.isoparse('2021-09-30 19:50:11.00'),
            parser.isoparse('2021-12-31 14:20:11.00'),
            parser.isoparse('2021-03-31 00:00:00.00'),
            parser.isoparse('2021-03-31 23:59:59.00'),
            parser.isoparse('2021-06-30 00:00:00.00'),
            parser.isoparse('2021-06-30 23:59:59.00'),
            parser.isoparse('2021-09-30 00:00:00.00'),
            parser.isoparse('2021-09-30 23:59:59.00'),
            parser.isoparse('2021-12-31 00:00:00.00'),
            parser.isoparse('2021-12-31 23:59:59.00'),
        ]
        for i in range(len(test_quarterly)):
            self.assertEqual(
                check_quarterly[i],
                self.env['to.base'].find_last_date_of_period(
                    period_name='quarterly', date=test_quarterly[i]
                ),
                "\nTest case TC07.03 - Test quarterly",
            )

        # Test biannually
        test_biannually = [
            parser.isoparse('2021-03-04 18:00:00.00'),
            parser.isoparse('2021-10-25 08:01:00.00'),
            parser.isoparse('2021-01-01 00:00:00.00'),
            parser.isoparse('2021-06-30 23:59:59.00'),
            parser.isoparse('2021-07-01 00:00:00.00'),
            parser.isoparse('2021-12-31 23:59:59.00'),
        ]
        check_biannually = [
            parser.isoparse('2021-06-30 18:00:00.00'),
            parser.isoparse('2021-12-31 08:01:00.00'),
            parser.isoparse('2021-06-30 00:00:00.00'),
            parser.isoparse('2021-06-30 23:59:59.00'),
            parser.isoparse('2021-12-31 00:00:00.00'),
            parser.isoparse('2021-12-31 23:59:59.00'),
        ]
        for i in range(len(test_monthly)):
            self.assertEqual(
                check_biannually[i],
                self.env['to.base'].find_last_date_of_period(
                    period_name='biannually', date=test_biannually[i]
                ),
                "\nTest case TC07.04 - Test biannually",
            )

    # TC08
    def test_period_iter(self):
        test_vals = [
            {
                'period_name': 'weekly',
                'dt_start': parser.isoparse('2021-02-01'),
                'dt_end': parser.isoparse('2021-03-01'),
            }
        ]
        check_vals = [
            [
                parser.isoparse('2021-02-01'),
                parser.isoparse('2021-02-07'),
                parser.isoparse('2021-02-14'),
                parser.isoparse('2021-02-21'),
                parser.isoparse('2021-02-28'),
                parser.isoparse('2021-03-01'),
            ]
        ]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].period_iter(**test_vals[i]),
                check_vals[i],
                '\nTest case TC08',
            )

    # TC09
    def test_get_days_of_month_from_date(self):
        test_vals = [
            parser.isoparse('2021-03-03'),
            parser.isoparse('2021-02-15'),
        ]
        check_vals = [31, 28]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].get_days_of_month_from_date(test_vals[i]),
                check_vals[i],
                "\nTest case TC09",
            )

    # TC10
    def test_get_day_of_year_from_date(self):
        test_vals = [
            parser.isoparse('2021-01-21').date(),
            parser.isoparse('2021-02-21').date(),
        ]
        check_vals = [21, 52]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].get_day_of_year_from_date(date=test_vals[i]),
                check_vals[i],
                "\nTest case TC10",
            )

    # TC11
    def test_get_days_between_dates(self):
        test_vals = [(parser.isoparse('2021-01-12'), parser.isoparse('2021-02-21'))]
        check_vals = [40]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].get_days_between_dates(*test_vals[i]),
                check_vals[i],
                "\nTest case TC11",
            )

    # TC12
    def test_get_months_between_dates(self):
        test_vals = [
            (parser.isoparse('2021-01-12'), parser.isoparse('2021-02-21')),
            (parser.isoparse('2021-01-12'), parser.isoparse('2021-01-15')),
        ]
        check_vals = [1.359447004608295, 0.0967741935483871]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].get_months_between_dates(*test_vals[i]),
                check_vals[i],
                "\nTest case TC12",
            )

    # TC13
    def test_get_weekdays_for_period(self):
        test_vals = [
            (parser.isoparse('2021-03-02'), parser.isoparse('2021-03-05')),
        ]
        check_vals = [
            {
                1: parser.isoparse('2021-03-02').date(),
                2: parser.isoparse('2021-03-03').date(),
                3: parser.isoparse('2021-03-04').date(),
                4: parser.isoparse('2021-03-05').date(),
            }
        ]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].get_weekdays_for_period(*test_vals[i]),
                check_vals[i],
                "\nTest case TC13",
            )

        test_invalid_vals = (
            parser.isoparse('2021-03-02'),
            parser.isoparse('2021-03-10'),
        )
        with self.assertRaises(ValidationError):
            self.env['to.base'].get_weekdays_for_period(*test_invalid_vals)

    # TC14
    def test_next_weekday(self):
        test_vals = [
            {'date': parser.isoparse('2021-03-02'), 'weekday': None},
            {'date': parser.isoparse('2021-03-04').date(), 'weekday': None},
            {'date': parser.isoparse('2021-03-01'), 'weekday': 2},
            {'date': parser.isoparse('2021-03-07'), 'weekday': 3},
        ]
        check_vals = [
            parser.isoparse('2021-03-09'),
            parser.isoparse('2021-03-11').date(),
            parser.isoparse('2021-03-03'),
            parser.isoparse('2021-03-11'),
        ]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].next_weekday(**test_vals[i]),
                check_vals[i],
                "\nTest case TC14",
            )

    # TC15
    def test_split_date(self):
        test_vals = [
            parser.isoparse('2020-12-24').date(),
            parser.isoparse('2021-03-01').date(),
        ]
        check_vals = [(2020, 12, 24), (2021, 3, 1)]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].split_date(test_vals[i]),
                check_vals[i],
                '\nTest case TC15',
            )

    # TC16
    def test_hours_time_string(self):
        test_vals = [2.0, 1.5, 1.333333]
        check_vals = ['02:00', '01:30', '01:20']
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].hours_time_string(test_vals[i]),
                check_vals[i],
                '\nTest case TC16',
            )

    # TC18
    def test_zip_dirs(self):
        pass

    # TC19
    def test_guess_lang(self):
        pass

    # TC20
    def test_strip_accents(self):
        test_vals = [
            'Đây là một câu tiếng việt có dấu.',
            'Đâylàmộtcâutiếngviệtcódấu.',
            'á à ả ã ạ ă ắ ằ ẳ ẵ ặ â ấ ầ ẩ ẫ ậ',
            'í ì ỉ ĩ ị',
            'ú ù ủ ũ ụ ư ứ ừ ử ữ ự',
            'é è ẻ ẽ ẹ ê ế ề ể ễ ệ',
            'ó ò ỏ õ ọ ô ố ồ ổ ỗ ộ ơ ớ ờ ở ỡ ợ',
            'ý ỳ ỷ ỹ ỵ',
            'đ',
            'Á À Ả Ã Ạ Ă Ắ Ằ Ẳ Ẵ Ặ Â Ấ Ầ Ẩ Ẫ Ậ',
            'Í Ì Ỉ Ĩ Ị',
            'Ú Ù Ủ Ũ Ụ Ư Ứ Ừ Ử Ữ Ự',
            'É È Ẻ Ẽ Ẹ Ê Ế Ề Ể Ễ Ệ',
            'Ó Ò Ỏ Õ Ọ Ô Ố Ồ Ổ Ỗ Ộ Ơ Ớ Ờ Ở Ỡ Ợ',
            'Ý Ỳ Ỷ Ỹ Ỵ',
            'Đ',
        ]
        check_vals = [
            'Day la mot cau tieng viet co dau.',
            'Daylamotcautiengvietcodau.',
            'a a a a a a a a a a a a a a a a a',
            'i i i i i',
            'u u u u u u u u u u u',
            'e e e e e e e e e e e',
            'o o o o o o o o o o o o o o o o o',
            'y y y y y',
            'd',
            'A A A A A A A A A A A A A A A A A',
            'I I I I I',
            'U U U U U U U U U U U',
            'E E E E E E E E E E E',
            'O O O O O O O O O O O O O O O O O',
            'Y Y Y Y Y',
            'D',
        ]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].strip_accents(test_vals[i]),
                check_vals[i],
                '\nTest case TC20',
            )

    # TC21
    def test_sum_digits(self):
        test_vals = (
            {'n': 178, 'number_of_digit_return': 2},
            {'n': 178, 'number_of_digit_return': 1},
        )
        check_vals = [16, 7]
        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].sum_digits(**test_vals[i]),
                check_vals[i],
                '\nTest case TC21',
            )

    # TC22
    def test_find_nearest_lucky_number(self):
        test_vals = (
            {'n': 12345, 'rounding': 2, 'round_up': False},
            {'n': 12345, 'rounding': 0, 'round_up': True},
        )
        check_vals = (11700, 12348)

        for i in range(len(test_vals)):
            self.assertEqual(
                self.env['to.base'].find_nearest_lucky_number(**test_vals[i]),
                check_vals[i],
                '\nTest case TC22',
            )
