import scrapy

class DeputadoSpider(scrapy.Spider):
  name = 'deputados'

  start_urls = ['https://www.camara.leg.br/deputados/quem-sao/resultado?search=&partido=&uf=&legislatura=56&sexo=F']

  def parse(self, response):
    urls = [
          "https://www.camara.leg.br/deputados/204528",
          "https://www.camara.leg.br/deputados/204545",
          "https://www.camara.leg.br/deputados/74057",
          "https://www.camara.leg.br/deputados/204353",
          "https://www.camara.leg.br/deputados/204400",
          "https://www.camara.leg.br/deputados/73696",
          "https://www.camara.leg.br/deputados/123756",
          "https://www.camara.leg.br/deputados/204509",
          "https://www.camara.leg.br/deputados/73701",
          "https://www.camara.leg.br/deputados/204374",
          "https://www.camara.leg.br/deputados/160589",
          "https://www.camara.leg.br/deputados/213762",
          "https://www.camara.leg.br/deputados/204507",
          "https://www.camara.leg.br/deputados/164360",
          "https://www.camara.leg.br/deputados/204369",
          "https://www.camara.leg.br/deputados/204380",
          "https://www.camara.leg.br/deputados/204462",
          "https://www.camara.leg.br/deputados/178928",
          "https://www.camara.leg.br/deputados/178939",
          "https://www.camara.leg.br/deputados/204459",
          "https://www.camara.leg.br/deputados/81297",
          "https://www.camara.leg.br/deputados/204434",
          "https://www.camara.leg.br/deputados/178994",
          "https://www.camara.leg.br/deputados/204421",
          "https://www.camara.leg.br/deputados/178989",
          "https://www.camara.leg.br/deputados/204525",
          "https://www.camara.leg.br/deputados/178945",
          "https://www.camara.leg.br/deputados/204357",
          "https://www.camara.leg.br/deputados/204535",
          "https://www.camara.leg.br/deputados/178961",
          "https://www.camara.leg.br/deputados/204360",
          "https://www.camara.leg.br/deputados/178946",
          "https://www.camara.leg.br/deputados/204534",
          "https://www.camara.leg.br/deputados/204464",
          "https://www.camara.leg.br/deputados/178901",
          "https://www.camara.leg.br/deputados/204466",
          "https://www.camara.leg.br/deputados/215044",
          "https://www.camara.leg.br/deputados/74784",
          "https://www.camara.leg.br/deputados/178866",
          "https://www.camara.leg.br/deputados/166402",
          "https://www.camara.leg.br/deputados/204458",
          "https://www.camara.leg.br/deputados/204471",
          "https://www.camara.leg.br/deputados/204430",
          "https://www.camara.leg.br/deputados/74398",
          "https://www.camara.leg.br/deputados/204540",
          "https://www.camara.leg.br/deputados/178956",
          "https://www.camara.leg.br/deputados/204428",
          "https://www.camara.leg.br/deputados/204432",
          "https://www.camara.leg.br/deputados/204453",
          "https://www.camara.leg.br/deputados/66179",
          "https://www.camara.leg.br/deputados/205535",
          "https://www.camara.leg.br/deputados/204377",
          "https://www.camara.leg.br/deputados/73943",
          "https://www.camara.leg.br/deputados/204529",
          "https://www.camara.leg.br/deputados/204565",
          "https://www.camara.leg.br/deputados/160639",
          "https://www.camara.leg.br/deputados/160641",
          "https://www.camara.leg.br/deputados/204467",
          "https://www.camara.leg.br/deputados/178925",
          "https://www.camara.leg.br/deputados/74075",
          "https://www.camara.leg.br/deputados/220008",
          "https://www.camara.leg.br/deputados/160575",
          "https://www.camara.leg.br/deputados/204407",
          "https://www.camara.leg.br/deputados/204354",
          "https://www.camara.leg.br/deputados/160598",
          "https://www.camara.leg.br/deputados/178966",
          "https://www.camara.leg.br/deputados/107283",
          "https://www.camara.leg.br/deputados/198197",
          "https://www.camara.leg.br/deputados/67138",
          "https://www.camara.leg.br/deputados/74848",
          "https://www.camara.leg.br/deputados/108338",
          "https://www.camara.leg.br/deputados/178839",
          "https://www.camara.leg.br/deputados/204468",
          "https://www.camara.leg.br/deputados/204546",
          "https://www.camara.leg.br/deputados/160534",
          "https://www.camara.leg.br/deputados/178832",
          "https://www.camara.leg.br/deputados/204375",
          "https://www.camara.leg.br/deputados/139285",
          "https://www.camara.leg.br/deputados/204405",
          "https://www.camara.leg.br/deputados/204410",]
    # for url in response.css('.lista-resultados__cabecalho > a::attr(href)').getall():
    for url in urls:
      yield response.follow(url, callback=self.parse_data, dont_filter=True)

  def parse_data(self, response):
    data = {}
    data['nome'] = response.css('.informacoes-deputado li:first-child::text').get().strip()

    ausencias_label = ['presença_plenario', 'ausencia_justificada_plenario', 'ausencia_plenario',
                 'presenca_comissao', 'ausencia_justificada_comissao', 'ausencia_comissao']
      

    ausencias_presencas = [int(r.strip().split()[0]) for r in response.css('.list-table__definition-description::text').getall()]
    for i in range(len(ausencias_presencas)):
      data[ausencias_label[i]] = ausencias_presencas[i]

    # data['data_nascimento'] = response.css('.informacoes-deputado li:nth-child(5)::text').get().strip()
    
    # data['quant_viagem'] = int(response.css('.recursos-beneficios-deputado-container li:nth-child(5) > div > a::text').get())
    # print(data)

    data['salario_bruto_par'] = response.css('.recursos-deputado ul > li:nth-child(2) a::text').getall()[1].split()[1]  

    next_page = response.css('.gasto .veja-mais a::attr(href)').getall()
    cota_parlamentar_page = next_page[0]
    verba_gabinete_page = next_page[1]
    
    yield scrapy.Request(cota_parlamentar_page, callback=self.parse_gastos_parlamentar, cb_kwargs={"data": data}, meta={'verba_gabinete_url': verba_gabinete_page})

  def parse_gastos_parlamentar(self, response, data):
    gastos = [price.strip().split()[1] for price in response.css('.numerico::text').getall()[1:]]
    data['gasto_total_par'] = gastos[0]

    gastos = gastos[1:len(gastos) - 1]    
    meses = ['gasto_jan_par', 'gasto_fev_par', 'gasto_mar_par', 'gasto_abr_par ', 'gasto_maio_par',
             'gasto_junho_par', 'gasto_jul_par', 'gasto_agosto_par', 'gasto_set_par',
             'gasto_out_par', 'gasto_nov_par', 'gasto_dez_par']

    # pode ser que ainda não haja informação para um determinado mês, por isso preenchemos com 0 inicialmente
    for mes in meses:
      data[mes] = "0"
    
    for i in range(len(gastos)):
      data[meses[i]] = gastos[i]

    yield response.follow(response.meta['verba_gabinete_url'], callback=self.parse_gastos_gabinete, cb_kwargs={"data": data})

  def parse_gastos_gabinete(self, response, data):
    meses = ['gasto_jan_gab', 'gasto_fev_gab', 'gasto_mar_gab', 'gasto_abr_gab ', 'gasto_maio_gab',
             'gasto_junho_gab', 'gasto_jul_gab', 'gasto_agosto_gab', 'gasto_set_gab',
             'gasto_out_gab', 'gasto_nov_gab', 'gasto_dez_gab']

    for mes in meses:
      data[mes] = "0"
    
    gastos_gabinete = response.css('.alinhar-direita:nth-child(3)::text').getall()[1:]
    for i in range(len(gastos_gabinete)):
      data[meses[i]] = gastos_gabinete[i]

    yield data
