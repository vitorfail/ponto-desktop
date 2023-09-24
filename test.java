import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class MinhaInterfaceJava {
    public static void main(String[] args) {
        // Criar uma janela
        JFrame janela = new JFrame("Minha Interface Java");
        janela.setSize(400, 200);
        janela.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Criar um painel
        JPanel painel = new JPanel();

        // Criar um botão
        JButton botao = new JButton("Clique-me!");
        
        // Criar um rótulo para exibir a mensagem
        JLabel rotulo = new JLabel();

        // Adicionar um ouvinte de ação ao botão
        botao.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                rotulo.setText("Você clicou no botão!");
            }
        });

        // Adicionar componentes ao painel
        painel.add(botao);
        painel.add(rotulo);

        // Adicionar o painel à janela
        janela.add(painel);

        // Tornar a janela visível
        janela.setVisible(true);
    }
}
