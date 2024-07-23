
from py2neo import *
import csv


##### 作者可能多个还没解决

# 注意每个数据结尾有\n

# Create your models here.
class DataToNeo4j(object):
    def __init__(self):
        self.nodes = None
        self.search_now = None
        self.attr_list = []
        self.attr_name = []
        self.attr_to_name = {}
        self.output_list = []
        self.key = None
        link = Graph("http://localhost:7474", auth=('neo4j', '123456'))  # 建立连接
        self.graph = link
        self.old_key = None
        self.wos = 'web of science'
        self.author = 'author'
        self.institution = 'institution'
        self.cooperate = 'cooperate'
        self.country = 'country'
        self.dict1 = {}
        self.matcher = NodeMatcher(link)  # 匹配关系的方法
        self.read_ordered()

        # self.clear()

    def read_ordered(self):
        file = open('order.txt', 'r', encoding='UTF-8-sig')
        for line in file:
            list_line = line.strip().split('\t')
            self.attr_list.append(list_line[0])
            self.attr_name.append(list_line[1])
            self.attr_to_name[list_line[0]] = list_line[1]
            self.dict1[list_line[0]] = 0

            # 清空数据库

    def clear(self):
        self.graph.delete_all()  # 清空数据库

    # 建立节点
    def create_cooperate_node(self):
        dict_node = {}
        dict_relation = {}

        for node in self.list_wos_node:
            print('处理第一个node')
            if node['C1']:
                country_list = node['C1'].strip().split('.\n  ')

                country_list[-1] = country_list[-1].strip('.')
                # 先创建国家节点
                country = []
                # 特殊情况 本身资料不全
                flag = 0
                for i in range(len(country_list)):
                    tmp = country_list[i].split(', ')
                    if len(tmp) == 1:
                        flag = 1
                        break
                    else:
                        country.append(tmp[-1])
                if flag:
                    continue

                for i in range(len(country)):
                    if country[i][-3:] == 'USA':
                        country[i] = 'USA'
                country = list(set(country))

                if len(country) == 1:
                    country_node = dict_node.get(repr(country[0]))
                    if country_node is None:
                        country_node = Node(self.country + self.cooperate, name=country[0], theme=self.key,
                                            number=1)
                        dict_node[repr(country[0])] = country_node
                    else:
                        country_node['number'] += 1
                else:
                    for i in range(len(country)):
                        for j in range(i + 1, len(country)):

                            country_node1 = dict_node.get(repr(country[i]))
                            if country_node1 is None:
                                country_node1 = Node(self.country + self.cooperate, theme=self.key,
                                                     name=country[i], number=1)
                                dict_node[repr(country[i])] = country_node1
                            else:
                                country_node1['number'] += 1
                            country_node2 = dict_node.get(repr(country[j]))
                            if country_node2 is None:
                                country_node2 = Node(self.country + self.cooperate, theme=self.key,
                                                     name=country[j], number=1)
                                dict_node[repr(country[j])] = country_node2
                            else:
                                country_node2['number'] += 1
                            Relation = dict_relation.get(
                                repr(country[i].strip()) + ' ' + repr(country[j].strip())) or \
                                       dict_relation.get(
                                           repr(country[j].strip()) + ' ' + repr(country[i].strip()))
                            if Relation is None:
                                Relation = Relationship(country_node1, "cooperate", country_node2)
                                Relation['number'] = 1
                                dict_relation[
                                    repr(country[i].strip()) + ' ' + repr(country[j].strip())] = Relation
                            else:
                                Relation['number'] += 1
                # print(country)
                # 创建作者和机构节点且开始连接关系
                for i in range(len(country_list)):
                    dict_data = {}
                    temp_list = country_list[i].split('] ')
                    # 如果只有一个作者
                    if len(temp_list) == 1:
                        if node['AF']:
                            dict_data['author'] = node['AF'].strip().split('\n  ')
                        elif node['BF']:
                            dict_data['author'] = node['BF'].strip().split('\n  ')
                        elif node['GP']:
                            dict_data['author'] = node['GP'].strip().split('\n  ')
                        elif node['BE']:
                            dict_data['author'] = node['BE'].strip().split('\n  ')
                        else:
                            dict_data['author'] = 'None'
                        temp_list = temp_list[0].split(', ')
                        # print('author ',dict_data['author'])
                        dict_data['institution'] = temp_list[0]
                        if temp_list[-1][-3:] == 'USA':
                            dict_data['country'] = 'USA'
                        else:
                            dict_data['country'] = temp_list[-1]
                    # 有多个作者
                    else:
                        dict_data['author'] = temp_list[0].strip().strip('[').split('; ')

                        temp_list = temp_list[1].split(', ')

                        dict_data['institution'] = temp_list[0]
                        if temp_list[-1][-3:] == 'USA':
                            dict_data['country'] = 'USA'
                        else:
                            dict_data['country'] = temp_list[-1]

                    # print('country ', dict_data['country'])

                    country_node = dict_node.get(repr(dict_data['country']))

                    # 添加机构节点
                    institution_node = dict_node.get(repr(dict_data['institution']))
                    if institution_node is None:
                        institution_node = Node(self.institution + self.cooperate, theme=self.key,
                                                name=dict_data['institution'],
                                                number=1)
                        dict_node[repr(dict_data['institution'])] = institution_node
                    else:
                        institution_node['number'] += 1
                    # 添加国家和机构的关系
                    Relation = dict_relation.get(
                        repr(dict_data['institution']) + ' ' + repr(dict_data['country']))
                    if Relation is None:
                        Relation = Relationship(institution_node, "contribute", country_node)
                        Relation['number'] = 1
                        dict_relation[
                            repr(dict_data['institution']) + ' ' + repr(dict_data['country'])] = Relation
                    else:
                        Relation['number'] = int(Relation['number']) + 1

                    if isinstance(dict_data['author'], list):
                        for author in dict_data['author']:
                            author_node = dict_node.get(repr(author))
                            if author_node is None:
                                author_node = Node(self.author + self.cooperate, theme=self.key, name=author,
                                                   number=1)
                                dict_node[repr(author)] = author_node
                            else:
                                author_node['number'] += 1
                            Relation = dict_relation.get(
                                repr(author) + ' ' + repr(dict_data['country']))
                            if Relation is None:
                                Relation = Relationship(author_node, "contribute", country_node)
                                Relation['number'] = 1
                                dict_relation[
                                    repr(author) + ' ' + repr(dict_data['country'])] = Relation
                            else:
                                Relation['number'] = int(Relation['number']) + 1
                    else:
                        author_node = dict_node.get(repr(dict_data['author']))
                        if author_node is None:
                            author_node = Node(self.author + self.cooperate, theme=self.key,
                                               name=dict_data['author'], number=1)
                            dict_node[repr(dict_data['author'])] = author_node
                        else:
                            author_node['number'] += 1
                        Relation = dict_relation.get(
                            repr(dict_data['author']) + ' ' + repr(dict_data['country']))
                        if Relation is None:
                            Relation = Relationship(author_node, "contribute", country_node)
                            Relation['number'] = 1
                            dict_relation[
                                repr(dict_data['author']) + ' ' + repr(dict_data['country'])] = Relation
                        else:
                            Relation['number'] = int(Relation['number']) + 1

        subgraph = Subgraph(list(dict_node.values()), list(dict_relation.values()))
        tx_ = self.graph.begin()
        tx_.create(subgraph)
        self.graph.commit(tx_)
        print("创建国家合作网络完成")
        self.output_list = []

    def create_node(self):

        if self.matcher.match('key').where('_.key={}'.format(repr(self.key))).first() is None:
            node = Node('key', key=self.key)
            self.graph.create(node)
        print('create node')
        self.del_key()
        self.dict_wos_node = {}
        self.list_wos_node = []
        before_insert_node = self.matcher.match(self.wos).where('_.theme={}'.format(repr(self.key)))
        if before_insert_node.first():
            for node in before_insert_node:
                self.list_wos_node.append(node)
                self.dict_wos_node[repr(node['UT'])] = 1

        for attr_dict in self.output_list:
            if self.dict_wos_node.get(repr(attr_dict['UT'])) is None:
                node = Node(self.wos, theme=self.key, **attr_dict)
                self.graph.create(node)
                self.dict_wos_node[repr(attr_dict['UT'])] = 1
                self.list_wos_node.append(node)

        dict_node = {}
        dict_relation = {}

        for node in self.list_wos_node:
            print('处理node……')
            if node['AF']:
                author_list = node['AF'].strip().split('\n  ')
            elif node['BF']:
                author_list = node['BF'].strip().split('\n  ')
            elif node['GP']:
                author_list = node['GP'].strip().split('\n  ')
            elif node['BE']:
                author_list = node['BE'].strip().split('\n  ')
            # elif node['CA']:
            #     author_list = node['CA'].strip().split('\n  ')
            else:

                print('作者暂缺:跳过')
                continue
                # print("++++++++++++")
                #
                # print(node)
                # assert 1 != 1
            if len(author_list) == 1:
                author_node1 = dict_node.get(repr(author_list[0].strip()))
                if author_node1 is None:
                    author_node1 = Node(self.author, theme=self.key, name=author_list[0].strip(), number=1)
                    dict_node[repr(author_list[0].strip())] = author_node1
                else:
                    author_node1['number'] += 1
            else:
                for i in range(len(author_list)):
                    for j in range(i + 1, len(author_list)):
                        author_node1 = dict_node.get(repr(author_list[i].strip()))
                        if author_node1 is None:
                            author_node1 = Node(self.author, theme=self.key, name=author_list[i].strip(), number=1)
                            dict_node[repr(author_list[i].strip())] = author_node1
                        else:
                            author_node1['number'] += 1

                        author_node2 = dict_node.get(repr(author_list[j].strip()))
                        if author_node2 is None:
                            author_node2 = Node(self.author, theme=self.key, name=author_list[j].strip(), number=1)
                            dict_node[repr(author_list[j].strip())] = author_node2
                        else:
                            author_node2['number'] += 1
                        Relation = dict_relation.get(
                            repr(author_list[i].strip()) + ' ' + repr(author_list[j].strip())) or \
                                   dict_relation.get(repr(author_list[j].strip()) + ' ' + repr(author_list[i].strip()))
                        if Relation is None:
                            Relation = Relationship(author_node1, "cooperate", author_node2)
                            Relation['number'] = 1
                            dict_relation[
                                repr(author_list[i].strip()) + ' ' + repr(author_list[j].strip())] = Relation
                        else:
                            Relation['number'] += 1

            if node['C3']:
                institution_list = node['C3'].strip().split(';')
                for i in range(len(institution_list)):
                    institution_list[i] = institution_list[i].strip().replace('\n  ', '').replace('\n', '')  # 更改
                institution_list = list(set(institution_list))
            if node['C3']:
                for i in range(len(institution_list)):
                    for j in range(i + 1, len(institution_list)):

                        institution_node1 = dict_node.get(repr(institution_list[i]))
                        if institution_node1 is None:
                            institution_node1 = Node(self.institution, theme=self.key, name=institution_list[i],
                                                     number=1)
                            dict_node[repr(institution_list[i])] = institution_node1
                        else:
                            institution_node1['number'] += 1

                        # if institution_list[i] == institution_list[j]:
                        #     institution_node1['pagerank'] += 1
                        #     continue

                        institution_node2 = dict_node.get(repr(institution_list[j]))
                        if institution_node2 is None:
                            institution_node2 = Node(self.institution, theme=self.key, name=institution_list[j],
                                                     number=1)
                            dict_node[repr(institution_list[j])] = institution_node2
                        else:
                            institution_node2['number'] += 1

                        Relation = dict_relation.get(
                            repr(institution_list[i].strip()) + ' ' + repr(institution_list[j].strip())) or \
                                   dict_relation.get(
                                       repr(institution_list[j].strip()) + ' ' + repr(institution_list[i].strip()))
                        if Relation is None:
                            Relation = Relationship(institution_node1, "cooperate", institution_node2)
                            Relation['number'] = 1
                            dict_relation[
                                repr(institution_list[i].strip()) + ' ' + repr(institution_list[j].strip())] = Relation
                        else:
                            Relation['number'] = int(Relation['number']) + 1

            if node['C1']:
                country_list = node['C1'].strip().split('.\n')  # 注意把本身结尾的\n去掉了

                for i in range(len(country_list)):
                    country_list[i] = country_list[i].split(',')[-1].strip().strip('.')
                for i in range(len(country_list)):
                    if country_list[i][-3:] == 'USA':
                        country_list[i] = 'USA'
                country_list = list(set(country_list))
                if len(country_list) == 1:
                    country_node1 = dict_node.get(repr(country_list[0]))
                    if country_node1 is None:
                        country_node1 = Node(self.country, theme=self.key, name=country_list[0], number=1)
                        dict_node[repr(country_list[0])] = country_node1
                    else:
                        country_node1['number'] += 1
                else:
                    for i in range(len(country_list)):
                        for j in range(i + 1, len(country_list)):

                            country_node1 = dict_node.get(repr(country_list[i]))
                            if country_node1 is None:
                                country_node1 = Node(self.country, theme=self.key, name=country_list[i], number=1)
                                dict_node[repr(country_list[i])] = country_node1
                            else:
                                country_node1['number'] += 1

                            if country_list[i] == country_list[j]:
                                continue

                            country_node2 = dict_node.get(repr(country_list[j]))
                            if country_node2 is None:
                                country_node2 = Node(self.country, theme=self.key, name=country_list[j], number=1)
                                dict_node[repr(country_list[j])] = country_node2
                            else:
                                country_node2['number'] += 1
                            Relation = dict_relation.get(
                                repr(country_list[i].strip()) + ' ' + repr(country_list[j].strip())) or \
                                       dict_relation.get(
                                           repr(country_list[j].strip()) + ' ' + repr(country_list[i].strip()))
                            if Relation is None:
                                Relation = Relationship(country_node1, "cooperate", country_node2)
                                Relation['number'] = 1
                                dict_relation[
                                    repr(country_list[i].strip()) + ' ' + repr(country_list[j].strip())] = Relation
                            else:
                                Relation['number'] = int(Relation['number']) + 1

        subgraph = Subgraph(list(dict_node.values()), list(dict_relation.values()))
        tx_ = self.graph.begin()
        tx_.create(subgraph)
        self.graph.commit(tx_)
        print("创建完成")

    # 查询版本的创建节点方法
    # def create_node(self):
    #     new_node = []
    #     for attr_dict in self.output_list:
    #         if self.matcher.match(self.wos).where('_.UT={}'.format(repr(attr_dict['UT']))).first() is None:
    #             node = Node(self.wos, **attr_dict)
    #             self.graph.create(node)
    #             new_node.append(node)
    #         else:
    #             print("重复数据")
    #     k = 0
    #     for node in new_node:
    #         print(k)
    #         k += 1
    #         if node['AF']:
    #             author_list = node['AF'].strip().split('\n')
    #         elif node['BF']:
    #             author_list = node['BF'].strip().split('\n')
    #         elif node['GP']:
    #             author_list = node['GP'].strip().split('\n')
    #         elif node['BE']:
    #             author_list = node['BE'].strip().split('\n')
    #         else:
    #             print("++++++++++++")
    #             print(node)
    #             assert 1 != 1
    #
    #         for i in range(len(author_list)):
    #             for j in range(i + 1, len(author_list)):
    #                 author_node1 = self.matcher.match(self.author).where(
    #                     '_.name={}'.format(repr(author_list[i].strip()))).first()
    #                 if author_node1 is None:
    #                     author_node1 = Node(self.author, name=author_list[i].strip(), pagerank=1)
    #                     self.graph.create(author_node1)
    #                 else:
    #                     author_node1['pagerank'] += 1
    #                     self.graph.push(author_node1)
    #                 author_node2 = self.matcher.match(self.author).where(
    #                     '_.name={}'.format(repr(author_list[j].strip()))).first()
    #                 if author_node2 is None:
    #                     author_node2 = Node(self.author, name=author_list[j].strip(), pagerank=1)
    #                     self.graph.create(author_node2)
    #                 else:
    #                     author_node2['pagerank'] += 1
    #                     self.graph.push(author_node2)
    #                 Relation = RelationshipMatcher(self.graph).match({author_node1, author_node2},
    #                                                                  r_type="cooperate").first()
    #                 if Relation is None:
    #                     Relation = Relationship(author_node1, "cooperate", author_node2)
    #                     Relation['number'] = 1
    #                     self.graph.create(Relation)
    #                 else:
    #                     Relation['number'] = int(Relation['number']) + 1
    #                     self.graph.push(Relation)
    #
    #         if node['C3']:
    #             institution_list = node['C3'].strip().split(';')
    #             for i in range(len(institution_list)):
    #                 institution_list[i] = institution_list[i].strip().replace('\n  ', '')
    #         if node['C3']:
    #             for i in range(len(institution_list)):
    #                 for j in range(i + 1, len(institution_list)):
    #
    #                     institution_node1 = self.matcher.match(self.institution).where(
    #                         '_.name={}'.format(repr(institution_list[i]))).first()
    #                     if institution_node1 is None:
    #                         institution_node1 = Node(self.institution, name=institution_list[i], pagerank=1)
    #                         self.graph.create(institution_node1)
    #                     else:
    #                         institution_node1['pagerank'] += 1
    #                         self.graph.push(institution_node1)
    #                     if institution_list[i] == institution_list[j]:
    #                         institution_node1['pagerank'] += 1
    #                         self.graph.push(institution_node1)
    #                         continue
    #
    #                     institution_node2 = self.matcher.match(self.institution).where(
    #                         '_.name={}'.format(repr(institution_list[j]))).first()
    #                     if institution_node2 is None:
    #                         institution_node2 = Node(self.institution, name=institution_list[j], pagerank=1)
    #                         self.graph.create(institution_node2)
    #                     else:
    #                         institution_node2['pagerank'] += 1
    #                         self.graph.push(institution_node2)
    #                     Relation = RelationshipMatcher(self.graph).match({institution_node1, institution_node2},
    #                                                                      r_type="cooperate").first()
    #                     if Relation is None:
    #                         Relation = Relationship(institution_node1, "cooperate", institution_node2)
    #                         Relation['number'] = 1
    #                         self.graph.create(Relation)
    #                     else:
    #                         Relation['number'] = int(Relation['number']) + 1
    #                         self.graph.push(Relation)
    #         if node['C1']:
    #             country_list = node['C1'].strip().split('.\n')
    #             for i in range(len(country_list)):
    #                 country_list[i] = country_list[i].split(',')[-1].strip()
    #
    #         if node['C1']:
    #             for i in range(len(country_list)):
    #                 for j in range(i + 1, len(country_list)):
    #                     if country_list[i][-3:] == 'USA':
    #                         country_list[i] = 'USA'
    #
    #                     if country_list[j][-3:] == 'USA':
    #                         country_list[j] = 'USA'
    #
    #                     country_node1 = self.matcher.match(self.country).where(
    #                         '_.name={}'.format(repr(country_list[i]))).first()
    #                     if country_node1 is None:
    #                         country_node1 = Node(self.country, name=country_list[i], pagerank=1)
    #                         self.graph.create(country_node1)
    #                     else:
    #                         country_node1['pagerank'] += 1
    #                         self.graph.push(country_node1)
    #
    #                     if country_list[i] == country_list[j]:
    #                         country_node1['pagerank'] += 1
    #                         self.graph.push(country_node1)
    #                         continue
    #
    #                     country_node2 = self.matcher.match(self.country).where(
    #                         '_.name={}'.format(repr(country_list[j]))).first()
    #                     if country_node2 is None:
    #                         country_node2 = Node(self.country, name=country_list[j], pagerank=1)
    #                         self.graph.create(country_node2)
    #                     else:
    #                         country_node2['pagerank'] += 1
    #                         self.graph.push(country_node2)
    #                     Relation = RelationshipMatcher(self.graph).match({country_node1, country_node2},
    #                                                                      r_type="cooperate").first()
    #                     if Relation is None:
    #                         Relation = Relationship(country_node1, "cooperate", country_node2)
    #                         Relation['number'] = 1
    #                         self.graph.create(Relation)
    #                     else:
    #                         Relation['number'] = int(Relation['number']) + 1
    #                         self.graph.push(Relation)
    #     print('创建节点成功')

    # 读取web of science的数据
    def read_wos_txt(self, txt_path):

        file = open(txt_path, 'r', encoding='UTF-8-sig')
        file.readline()
        file.readline()
        output_list = []
        wait_list = []
        name = []
        for line in file:
            list_line = line.split(" ")
            if list_line[0] == 'PT':
                name.append(list_line[0])
                tmp = [list_line[1]]
                continue
            if list_line[0] == '\n':
                continue

            if len(list_line[0]) == 2 or list_line[0] == 'ER\n':
                if list_line[0] != 'ER\n':
                    ### ***********
                    if list_line[0] not in self.attr_to_name.keys():
                        print(list_line[0])
                    name.append(list_line[0])

                if wait_list:
                    sentence = ''
                    for wait_line in wait_list:
                        for i in wait_line:
                            sentence = sentence + i + ' '  # 加的空格也包括换行后的前置空格

                    sentence = sentence.strip(' ')
                    tmp.append(sentence)
                wait_list = [list_line[1:]]
            else:
                if list_line[0] == '':
                    wait_list.append(list_line[1:])
                else:
                    wait_list.append(list_line)

            if list_line[0] == 'ER\n':
                assert len(name) == len(tmp)
                dict_tmp = {}
                for i in range(len(name)):
                    dict_tmp[name[i]] = tmp[i]
                output_list.append(dict_tmp)
                wait_list = []
                name = []
        file.close()
        print('读取数据成功')
        self.output_list += output_list

    def write_wos_txt(self, output_path, doc_type):
        if doc_type == 'txt':
            with open(output_path, 'w', encoding='UTF-8-sig') as f:
                f.write("FN Clarivate Analytics Web of Science\n")
                f.write("VR 1.0\n")
                for node in self.search_now:
                    for i in range(len(self.attr_list)):
                        if node[self.attr_list[i]] is not None:
                            f.write(self.attr_list[i] + " ")
                            f.write(node[self.attr_list[i]])
                    f.write('ER\n')
                    f.write('\n')
                f.write("EF")
        else:
            with open(output_path, 'w', encoding='UTF-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.attr_name[0:-1])
                for node in self.search_now:
                    write_row = []
                    for i in range(len(self.attr_list)):
                        if node[self.attr_list[i]] is not None:
                            write_row.append(node[self.attr_list[i]].strip())
                        else:
                            write_row.append('None')
                    writer.writerow(write_row)

    def get_example(self, label):
        """
        self.nodes = self.matcher.match(label)
        self.search_now = []
        self.search_index = 0
        for node in self.nodes:

        """
        self.example_attr = [
            {'id': 'a', 'name': '搜索', 'child': [{'id': 'user', 'name': '作者'}, {'id': 'key', 'name': '关键词'},
                                                  {'id': 'title', 'name': '题目'}]},
            {'id': 'b', 'name': '上传', 'child': [{'id': 'upload', 'name': '上传论文文件'}]}]
        return self.example_attr

    def search(self, num, size, keyword):
        key_list = keyword.strip().split(' ')

        for i in range(len(key_list)):
            key_list[i] = key_list[i].lower()
        search_key = ''
        for i in range(len(key_list) - 1):
            search_key += key_list[i] + ' '
        search_key += key_list[len(key_list) - 1]

        def judge(judge_node, judge_list):
            for judge_item in judge_list:
                if judge_node['ID'] is not None:
                    if judge_item in judge_node['ID'].lower():
                        continue
                if judge_node['DE'] is not None:
                    if judge_item in judge_node['DE'].lower():
                        continue
                if judge_node['AB'] is not None:
                    if judge_item in judge_node['AB'].lower():
                        continue
                if judge_node['MA'] is not None:
                    if judge_item in judge_node['MA'].lower():
                        continue
                if judge_node['TI'] is not None:
                    if judge_item in judge_node['TI'].lower():
                        continue
                if judge_node['SE'] is not None:
                    if judge_item in judge_node['SE'].lower():
                        continue
                if judge_node['CT'] is not None:
                    if judge_item in judge_node['CT'].lower():
                        continue
                if judge_node['SC'] is not None:
                    if judge_item in judge_node['SC'].lower():
                        continue
                return False
            return True

        if keyword != self.old_key:
            self.search_now = []
            self.old_key = keyword
            self.search_index = num
            self.search_size = size
            nodes = self.matcher.match(self.wos).where('_.theme={}'.format(repr(search_key)))
            if nodes.first():
                for node in nodes:
                    self.search_now.append(node)
            else:
                self.nodes = self.matcher.match(self.wos)
                for node in self.nodes:
                    if judge(node, key_list):
                        self.search_now.append(node)

        """
        attr = []
        value = []
        for i in range(len(self.attr_list)):
            if self.search_now[self.search_index][self.attr_list[i]] is not None:
                attr.append(self.attr_to_name[self.attr_list[i]])
                value.append(self.search_now[self.search_index][self.attr_list[i]])
        """
        self.search_index = num
        self.search_size = size
        title = []
        author = []
        address = []
        for item in self.search_now[(num - 1) * size:num * size]:
            if item['TI']:
                title.append(item['TI'])
            elif item['SE']:
                title.append(item['SE'])
            elif item['CT']:
                title.append(item['CT'])
            else:
                title.append("None")
            if item['AF']:
                author.append(item['AF'])
            elif item['BF']:
                author.append(item['BF'])
            elif item['GP']:
                author.append(item['GP'])
            elif item['BE']:
                author.append(item['BE'])
            else:
                author.append("None")
            if item['RP']:
                address.append(item['RP'])
            else:
                address.append("None")

        return title, author, address, len(
            self.search_now)

    def getdetail(self, title):
        self.node = self.matcher.match(self.wos).where('_.TI={}'.format(repr(title))).first() \
                    or self.matcher.match(self.wos).where('_.SE={}'.format(repr(title))).first() \
                    or self.matcher.match(self.wos).where('_.CT={}'.format(repr(title))).first()
        attr = []
        value = []
        if self.node:

            for i in range(len(self.attr_list)):
                if self.node[self.attr_list[i]] is not None:
                    attr.append(self.attr_to_name[self.attr_list[i]])
                    value.append(self.node[self.attr_list[i]])
        return attr, value

    def statistics(self):
        nodes = self.matcher.match(self.wos)
        self.author_set = set()
        self.institution_set = set()
        self.author_num = 0
        self.institution_num = 0
        self.paper_num = len(nodes)
        for node in nodes:
            if node['AF']:
                author_list = node['AF'].strip().split('\n')
                self.author_set = self.author_set.union(set(author_list))
            elif node['BF']:
                author_list = node['BF'].strip().split('\n')
                self.author_set = self.author_set.union(set(author_list))
            elif node['GP']:
                author_list = node['GP'].strip().split('\n')
                self.author_set = self.author_set.union(set(author_list))
            elif node['BE']:
                author_list = node['BE'].strip().split('\n')
                self.author_set = self.author_set.union(set(author_list))
            if node['C3']:
                institution_list = node['C3'].strip().split(';')
                self.institution_set = self.institution_set.union(set(institution_list))
        return {'paper': len(nodes), 'author': len(self.author_set), 'institution': len(self.institution_set)}

    def get_country(self, key):
        nodes = self.matcher.match(self.country + self.cooperate).where('_.theme={}'.format(repr(key)))
        country_list = []
        for node in nodes:
            country_list.append(node['name'])
        return country_list

    def get_keyword(self):
        nodes = self.matcher.match('key')
        keyword_list = []
        for node in nodes:
            keyword_list.append(node['key'])
        return keyword_list

    def del_key(self):
        self.graph.run("MATCH (n:`author`{theme:" + repr(self.key) + "}) detach delete n")
        self.graph.run("MATCH (n:`authorcooperate`{theme:" + repr(self.key) + "}) detach delete n")
        self.graph.run("MATCH (n:`country`{theme:" + repr(self.key) + "}) detach delete n")
        self.graph.run("MATCH (n:`countrycooperate`{theme:" + repr(self.key) + "}) detach delete n")
        self.graph.run("MATCH (n:`institution`{theme:" + repr(self.key) + "}) detach delete n")
        self.graph.run("MATCH (n:`institutioncooperate`{theme:" + repr(self.key) + "}) detach delete n")
