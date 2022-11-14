import scrapy

class DeputadoSpider(scrapy.Spider):
  name = 'deputados'
  data = {}

  start_urls = ['https://www.camara.leg.br/deputados/204507']

  def parse(self, response):

    self.data['nome'] = response.css('.informacoes-deputado li:first-child::text').get().strip()

    ausencias_label = ['presença_plenario', 'ausencia_justificada_plenario', 'ausencia_plenario',
                 'presenca_comissao', 'ausencia_justificada_comissao', 'ausencia_comissao']
      

    ausencias_presencas = [int(r.strip().split()[0]) for r in response.css('.list-table__definition-description::text').getall()]
    for i in range(len(ausencias_presencas)):
      self.data[ausencias_label[i]] = ausencias_presencas[i]

    self.data['data_nascimento'] = response.css('.informacoes-deputado li:nth-child(5)::text').get().strip()
    
    self.data['quant_viagem'] = int(response.css('.recursos-beneficios-deputado-container li:nth-child(5) > div > a::text').get())
    print(self.data)

    next_page = response.css('.gasto .veja-mais a::attr(href)').getall()
    cota_parlamentar_page = next_page[0]
    verba_gabinete_page = next_page[1]
    yield response.follow(cota_parlamentar_page, callback=self.parse_gastos_parlamentar, meta={'verba_gabinete_url': verba_gabinete_page})

    self.data['salario_bruto_par'] = response.css('.recursos-deputado ul > li:nth-child(2) a::text').getall()[1].split()[1]
  

  def parse_gastos_parlamentar(self, response):
    gastos = [price.strip().split()[1] for price in response.css('.numerico::text').getall()[1:]]
    
    gasto_total_par = gastos[-1]
    self.data['gasto_total_par'] = gasto_total_par

    gastos = gastos[1:len(gastos) - 1]    
    meses = ['gasto_jan_par', 'gasto_fev_par', 'gasto_mar_par', 'gasto_abr_par ', 'gasto_maio_par',
             'gasto_junho_par', 'gasto_jul_par', 'gasto_agosto_par', 'gasto_set_par',
             'gasto_out_par', 'gasto_nov_par', 'gasto_dez_par']

    # pode ser que ainda não haja informação para um determinado mês, por isso preenchemos com 0 inicialmente
    for mes in meses:
      self.data[mes] = "0"
    
    for i in range(len(gastos)):
      self.data[meses[i]] = gastos[i]

    
    yield response.follow(response.meta['verba_gabinete_url'], callback=self.parse_gastos_gabinete)

  def parse_gastos_gabinete(self, response):
    meses = ['gasto_jan_gab', 'gasto_fev_gab', 'gasto_mar_gab', 'gasto_abr_gab ', 'gasto_maio_gab',
             'gasto_junho_gab', 'gasto_jul_gab', 'gasto_agosto_gab', 'gasto_set_gab',
             'gasto_out_gab', 'gasto_nov_gab', 'gasto_dez_gab']

    for mes in meses:
      self.data[mes] = "0"
    
    gastos_gabinete = response.css('.alinhar-direita:nth-child(3)::text').getall()[1:]
    for i in range(len(gastos_gabinete)):
      self.data[meses[i]] = gastos_gabinete[i]

    yield self.data
