from django.db import models


class TenderType(models.Model):
    """ Тип закупки. """

    name = models.CharField(
        verbose_name='Наименование типа закупки',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тип закупки'
        verbose_name_plural = 'Типы закупки'

    def __str__(self):
        return self.name


class ObjectType(models.Model):
    """ Тип объекта закупки. """

    name = models.CharField(
        verbose_name='Наименование объекта закупки',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Тип объекта закупки'
        verbose_name_plural = 'Типы объекта закупки'

    def __str__(self):
        return self.name


class Region(models.Model):
    """ Регион организатора/заказчика. """

    name = models.CharField(
        verbose_name='Наименование региона',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return self.name


class JuridicalPerson(models.Model):
    """ Юридическое лицо (организатор/заказчик). """

    name = models.TextField(
        verbose_name='Наименование юрлица',
    )
    short_name = models.TextField(
        verbose_name='Краткое наименование',
        null=True
    )
    registration_date = models.DateTimeField(
        verbose_name='Дата регистрации'
    )
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=20,
        unique=True
    )
    ogrn = models.CharField(
        verbose_name='ОГРН',
        max_length=20
    )
    kpp = models.CharField(
        verbose_name='КПП',
        max_length=20
    )
    web_site = models.URLField(
        verbose_name='Адрес web сайта',
        null=True
    )
    eis_number = models.CharField(
        verbose_name='Номер в ЕИС',
        max_length=20
    )
    telephone = models.CharField(
        verbose_name='Телефон',
        max_length=20,
        null=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта'
    )
    fax = models.CharField(
        verbose_name='Факс',
        max_length=20,
        null=True
    )
    contact_person = models.CharField(
        verbose_name='Контактное лицо',
        max_length=100
    )
    address = models.TextField(
        verbose_name='Юридический адрес',
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        related_name='juridical_persons',
        verbose_name='Регион',
        null=True
    )

    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    def __str__(self):
        return self.name[:50]


class Tender(models.Model):
    """ Тендер. """

    number = models.CharField(
        verbose_name='Номер закупки',
        max_length=100,
        unique=True
    )
    tender_type = models.ForeignKey(
        TenderType,
        on_delete=models.SET_NULL,
        related_name='tenders',
        verbose_name='Тип закупки',
        null=True
    )
    title = models.TextField(
        verbose_name='Наименование закупки',
        db_index=True
    )
    price = models.FloatField(
        verbose_name='Сумма закупки (руб.)'
    )
    start_date = models.DateTimeField(
        verbose_name='Дата начала'
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания'
    )
    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.SET_NULL,
        related_name='tenders',
        verbose_name='Тип объекта закупки',
        null=True
    )
    organizer = models.ForeignKey(
        JuridicalPerson,
        on_delete=models.SET_NULL,
        related_name='organizer_tenders',
        verbose_name='Организатор',
        null=True
    )
    customer = models.ForeignKey(
        JuridicalPerson,
        on_delete=models.SET_NULL,
        related_name='customer_tenders',
        verbose_name='Заказчик',
        null=True
    )
    customer_region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        related_name='tenders',
        verbose_name='Регион заказчика',
        null=True
    )

    class Meta:
        verbose_name = 'Тендер'
        verbose_name_plural = 'Тендеры'
        ordering = ('-start_date',)

    def __str__(self):
        return self.number + ' ' + self.title[:50]


class TenderItem(models.Model):
    """ Предмет закупки/контракта. """

    code = models.TextField(
        verbose_name='Код предмета по ОКПД',
    )
    title = models.TextField(
        verbose_name='Наименование предмета',
        db_index=True
    )
    quantity = models.FloatField(
        verbose_name='Количество'
    )
    price = models.FloatField(
        verbose_name='Стоимость'
    )
    tender = models.ForeignKey(
        Tender,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Тендер предмета',
        null=True
    )

    class Meta:
        verbose_name = 'Предмет закупки/контакта'
        verbose_name_plural = 'Предметы закупки/контакта'
        constraints = [
            models.UniqueConstraint(
                fields=('code', 'title', 'quantity', 'price', 'tender'),
                name='unique_tender_item'
            )
        ]

    def __str__(self):
        return self.code
