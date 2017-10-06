# -*- coding: utf-8 -*-
class Tipo():
    
    def __init__(self, nome, nome_arquivo ):
        self.nome_arquivo = nome_arquivo
        self.nome = nome

    @staticmethod
    def bar():
        return Tipo("bar", "bar.html")

    @staticmethod
    def banda():
        return Tipo("banda", "bar.html")

    def __eq__(self,other):
        return self.nome == other.nome
