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


class Organizer(models.Model):
    """ Организатор. """

    name = models.TextField(
        verbose_name='Наименование организатора',
        unique=True
    )

    class Meta:
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'

    def __str__(self):
        return self.name


class Customer(models.Model):
    """ Заказчик. """

    name = models.TextField(
        verbose_name='Наименование заказчика',
        unique=True
    )

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.name


class Region(models.Model):
    """ Регион заказчика. """

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
        Organizer,
        on_delete=models.SET_NULL,
        related_name='tenders',
        verbose_name='Организатор',
        null=True
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name='tenders',
        verbose_name='Заказчик',
        null=True
    )
    region = models.ForeignKey(
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
        return str(self.number) + ' ' + self.title[:50]
